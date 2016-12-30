from pprint import pprint
from myslicelib.model.authority import Authority as myslicelibAuthority
from myslicelib.query import q
from myslice.db.activity import Object, ObjectType
from myslice import db
from myslice.db.user import User
from myslice.lib import Status
from myslice.lib.util import format_date
from xmlrpc.client import Fault as SFAError

class AuthorityException(Exception):
    def __init__(self, errors):
        self.stack = errors

class Authority(myslicelibAuthority):

    def __init__(self, data = {}):
        data = data if data is not None else {}
        data['domains'] = data.get('domains',[])
        super(Authority, self).__init__(data)

    def handleDict(self, key):
        new_elms = []
        tmp_elms = []
        for u in self.getAttribute(key):
            if isinstance(u, dict) and 'id' not in u:
                new_elms.append(u)
            elif isinstance(u, dict):
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

        result = { **(self.dict()), **result['data'][0]}
        # add status if not present and update on db
        if not 'status' in result:
            result['status'] = Status.ENABLED
            result['enabled'] = format_date()

        db.authorities(dbconnection, result, self.id)

        # New Authority created
        if current is None:
            current = db.get(dbconnection, table='authorities', id=self.id)

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

            db.users(dbconnection, user.dict())

        if modified:
            result = super(Authority, self).save(setup)
            errors = result['errors']
            if errors:
                raise AuthorityException(errors)

        return True

    def delete(self, dbconnection, setup=None):
        # Get Authority from local DB 
        # to update the pi_users after Save
        current = db.get(dbconnection, table='authorities', id=self.id)

        result = super(Authority, self).delete(setup)
        errors = result['errors']
        if errors:
            raise AuthorityException(errors)

        db.delete(dbconnection, 'authorities', self.id)

        for u in current['users']:
            db.delete(dbconnection, 'users', u)
        for u in current['pi_users']:
            user = q(User).id(u).get().first()
            if user:
                user = user.merge(dbconnection)
                db.users(dbconnection, user.dict())

        return True
