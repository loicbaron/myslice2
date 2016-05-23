from myslicelib.model.authority import Authority as myslicelibAuthority
from myslicelib.query import q
from myslice.db.activity import Object, ObjectType
from myslice import db
from myslice.db.user import User
from xmlrpc.client import Fault as SFAError


class Authority(myslicelibAuthority):

    def save(self, dbconnection, setup=None):
        result = super(Authority, self).save(setup)
        
        if result['errors']:
            raise Exception('errors: %s' % result['errors'] )
        else:
            result = { **(self.attributes()), **result['data'][0]}
            db.authorities(dbconnection, result, self.id)
            
            for user in self.pi_users:
                db.users(dbconnection, q(User).id(user).get().dict()) 
            return True

    def delete(self, dbconnection, setup=None):
        result = super(Authority, self).delete(setup)
        
        if result['errors']:
            raise Exception('errors: %s' % result['errors'])
        else:
            db.delete(dbconnection, 'authorities', self.id)

            for user in self.pi_users:
                db.users(dbconnection, q(User).id(user).get().dict()) 
            return True



