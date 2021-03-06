import logging
from pprint import pprint
from myslicelib.model.authority import Authority as myslicelibAuthority
from myslicelib.query import q
from myslice.db.activity import Object, ObjectType
from myslice import db
from myslice.db.user import User
from myslice.lib import Status
from myslice.lib.util import format_date
from xmlrpc.client import Fault as SFAError

logger = logging.getLogger('myslice.db.authority')

class AuthorityException(Exception):
    def __init__(self, errors):
        self.stack = errors

class Authority(myslicelibAuthority):

    def __init__(self, data = {}):
        # initialize the object with its id
        if isinstance(data, str):
            data = db.authorities(id=data)

        data = data if data is not None else {}
        data['domains'] = data.get('domains',[])
        super(Authority, self).__init__(data)

    def handleDict(self, key):
        new_elms = []
        tmp_elms = []
        for u in self.getAttribute(key):
            if isinstance(u, dict) and 'id' not in u:
                new_elms.append(u)
            elif isinstance(u, dict) and 'id' in u:
                tmp_elms.append(u['id'])
            else:
                tmp_elms.append(u)
        self.setAttribute(key, tmp_elms) 
        return new_elms

    def save(self, dbconnection, setup=None):
        # Get Authority from local DB 
        # to update the pi_users after Save
        current = db.get(dbconnection, table='authorities', id=self.id)

        new_users = self.handleDict('users')
        new_pi_users = self.handleDict('pi_users')

        result = super(Authority, self).save(setup)
        errors = result['errors']
        if errors:
            raise AuthorityException(errors)

        logger.debug(result)

        result = { **(self.dict()), **result['data'][0]}
        # add status if not present and update on db
        if not 'status' in result:
            result['status'] = Status.ENABLED
            result['enabled'] = format_date()

        # New Authority created
        if current is None:
            db.authorities(dbconnection, result)
            current = db.get(dbconnection, table='authorities', id=self.id)
        # Update existing authority
        else:
            db.authorities(dbconnection, result, self.id)

        # Create new users under a New Authority
        # Otherwise users are created with User.save()
        for u in new_users:
            if isinstance(u, dict):
                if not "email" in u:
                    raise Warning("user has no email can not be created")
                user = db.get(dbconnection, table='users', filter={'email':u['email']}, limit=1)
                # If the user doesn't exit, create it
                if not user:
                    user = User(u)
                    user.setAttribute('authority', self.id)
                    userCreated = user.save(dbconnection)
                    if not userCreated:
                        raise Warning("user has not been created")
                    self.users.append(user.id)
                    modified = True

        # Grant or Revoke PI Rights
        current['pi_users'] = current.get('pi_users', [])
        pi_users = current['pi_users'] + self.getAttribute('pi_users') + new_pi_users
        modified = False
        for u in pi_users:
            if isinstance(u, dict):
                if not "email" in u:
                    raise Warning("pi_user has no email can not be added as PI")
                user = db.get(dbconnection, table='users', filter={'email':u['email']}, limit=1)
                if not user:
                    raise Warning("user does not exist, can't be PI")
                else:
                    user = User(user[0])
            else:
                user = q(User).id(u).get().first()
                user = user.merge(dbconnection)

            # REMOVE PI Rights
            if user.id not in self.getAttribute('pi_users') and not any(d['email'] == user.email for d in new_pi_users):
                self.removePi(user)
                modified = True
            # GRANT PI Rights
            elif user.id not in current['pi_users']:
                self.addPi(user)
                modified = True
            logger.debug("Update user %s in Authority save()" % u)
            logger.debug(user)
            db.users(dbconnection, user.dict(), user.id)

        if modified:
            result = super(Authority, self).save(setup)
            errors = result['errors']
            if errors:
                raise AuthorityException(errors)
            result = { **(self.dict()), **result['data'][0]}
            # add status if not present and update on db
            if not 'status' in result:
                result['status'] = Status.ENABLED
                result['enabled'] = format_date()
            db.authorities(dbconnection, result, self.id)

        return True

    def delete(self, dbconnection, setup=None):
        logger.debug("Delete Authority %s" % self.id)
        # Get Authority from local DB 
        # to update the pi_users after Save
        logger.debug("Get current object")
        current = db.get(dbconnection, table='authorities', id=self.id)
        logger.debug("Delete sent to myslicelib")
        result = super(Authority, self).delete(setup)
        logger.debug("result from myslicelib")
        logger.debug(result)
        errors = result['errors']
        logger.debug("checking errors")
        if errors:
            raising = True
            for err in errors:
                if "Record not found" in err['exception']:
                    raising = False
                    break
            if raising:
                raise AuthorityException(errors)
        logger.debug("Delete Authority from local DB")
        db.delete(dbconnection, 'authorities', self.id)
        logger.debug("Delete users of the Authority from local DB")
        for u in current['users']:
            logger.debug("Delete user %s" % u)
            db.delete(dbconnection, 'users', u)
        logger.debug("Update PI users of the Authority in local DB")
        for u in current['pi_users']:
            logger.debug("Get user %s" % u)
            user = q(User).id(u).get().first()
            if user:
                logger.debug("Update user %s in Authority delete()" % u)
                logger.debug(user)
                user = user.merge(dbconnection)
                db.users(dbconnection, user.dict(), user.id)

        return True
