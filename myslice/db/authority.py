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

    def save(self, dbconnection, setup=None):
        result = super(Authority, self).save(setup)
        errors = result['errors']
        
        result = { **(self.dict()), **result['data'][0]}
        # add status if not present and update on db
        if not 'status' in result:
            result['status'] = Status.ENABLED
            result['enabled'] = format_date()

        db.authorities(dbconnection, result, self.id)

        # Get Authority from local DB 
        # to update the pi_users after Save
        current = db.get(dbconnection, table='authorities', id=self.id)

            
        for user in current['pi_users']:
            user = q(User).id(u).get().first()
            user = user.merge(dbconnection)
            db.users(dbconnection, user.dict())
        for user in current['users']:
            user = q(User).id(u).get().first()
            user = user.merge(dbconnection)
            db.users(dbconnection, user.dict())

        if errors:
            raise AuthorityException(errors)
        else:
            return True

    def delete(self, dbconnection, setup=None):
        result = super(Authority, self).delete(setup)
        errors = result['errors']
        
        db.delete(dbconnection, 'authorities', self.id)

        # Get Authority from local DB 
        # to update the pi_users after Save
        current = db.get(dbconnection, table='authorities', id=self.id)
        for user in current['pi_users']:
            user = q(User).id(u).get().first()
            user = user.merge(dbconnection)
            db.users(dbconnection, user.dict())
        for user in current['users']:
            user = q(User).id(u).get().first()
            user = user.merge(dbconnection)
            db.users(dbconnection, user.dict())

        if errors:
            raise AuthorityException(errors)
        else:
            return True
