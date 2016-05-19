from myslicelib.model.project import Project as myslicelibProject
from myslicelib.query import q
from myslice import db
from myslice.db.activity import Object, ObjectType
from myslice.db.user import User
from xmlrpc.client import Fault as SFAError

class Project(myslicelibProject):

    def save(self, dbconnection, setup=None):
        result = super(Project, self).save(setup)
        
        if result['errors']:
            raise Exception('errors: %s' % result['errors'] )
        else:
            result = { **(self.attributes()), **result['data'][0]}
            db.projects(dbconnection, result, self.id)
            
            for user in self.pi_users:
                db.users(dbconnection, q(User).id(user).get().dict()) 
            return True

    def delete(self, dbconnection,  setup=None):
        result = super(Project, self).delete(setup)
        
        if result['errors']:
            raise Exception('errors: %s' % result['errors'])
        else:
            db.delete(dbconnection, 'projects', self.id)

            for user in self.pi_users:
                db.users(dbconnection, q(User).id(user).get().dict()) 
            return True



