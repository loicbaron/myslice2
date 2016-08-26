from pprint import pprint

from myslicelib.model.project import Project as myslicelibProject
from myslicelib.query import q
from myslice import db
from myslice.db.activity import Object, ObjectType
from myslice.db.user import User
from myslice.db.slice import Slice
from myslice.lib import Status
from myslice.lib.util import format_date
from xmlrpc.client import Fault as SFAError

class ProjectException(Exception):
    def __init__(self, errors):
        self.stack = errors

class Project(myslicelibProject):

    def save(self, dbconnection, setup=None):
        result = super(Project, self).save(setup)
        errors = result['errors']

        result = { **(self.dict()), **result['data'][0]}
        # add status if not present and update on db
        if not 'status' in result:
            result['status'] = Status.ENABLED
            result['enabled'] = format_date()
        db.projects(dbconnection, result, self.id)

        # Get Project from local DB 
        # to update the pi_users after Save
        current = db.get(dbconnection, table='projects', id=self.id)
           
        for u in current['pi_users']:
            user = q(User).id(u).get().first()
            user = user.merge(dbconnection)
            db.users(dbconnection, user.dict())

        # update slices after Save
        for s in current['slices']:
            sl = q(Slice).id(s).get().first()
            db.slices(dbconnection, sl.dict())

        if errors:
            raise ProjectException(errors)
        else:
            return True

    def addPi(self, user, setup=None):
        self.appendAttribute('pi_users', user.id)
        return self

    def removePi(self, user, setup=None):
        self.setAttribute('pi_users', list(set(self.getAttribute('pi_users')) - set([user.id])))
        return self

    def delete(self, dbconnection,  setup=None):
        result = super(Project, self).delete(setup)
        errors = result['errors']

        db.delete(dbconnection, 'projects', self.id)

        # Get Project from local DB 
        # to update the pi_users after Save
        current = db.get(dbconnection, table='projects', id=self.id)
        for user in current['pi_users']:
            user = q(User).id(u).get().first()
            user = user.merge(dbconnection)
            db.users(dbconnection, user.dict())
        if errors:
            raise ProjectException(errors)
        else:
            return True
