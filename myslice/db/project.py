import logging
from pprint import pprint

from myslice import myslicelibsetup

from myslicelib.model.project import Project as myslicelibProject
from myslicelib.query import q
from myslice import db
from myslice.db.activity import Object, ObjectType
from myslice.db.user import User
from myslice.db.slice import Slice
from myslice.lib import Status
from myslice.lib.util import format_date
from xmlrpc.client import Fault as SFAError

logger = logging.getLogger('myslice.db.project')

class ProjectException(Exception):
    def __init__(self, errors):
        self.stack = errors

class Project(myslicelibProject):

    def save(self, dbconnection, setup=None):
        # Get Project from local DB 
        # to update the pi_users after Save
        current = db.get(dbconnection, table='projects', id=self.id)

        result = super(Project, self).save(setup)
        errors = result['errors']

        if errors:
            raise ProjectException(errors)

        result = { **(self.dict()), **result['data'][0]}
        # add status if not present and update on db
        if not 'status' in result:
            result['status'] = Status.ENABLED
            result['enabled'] = format_date()

        # New Project created
        if current is None:
            db.projects(dbconnection, result)
            current = db.get(dbconnection, table='projects', id=self.id)
        # Update existing project
        else:
            db.projects(dbconnection, result, self.id)

        # update pi_users after Save
        pi_users = list(set(current['pi_users']) | set(self.getAttribute('pi_users')))
        for u in pi_users:
            user = q(User).id(u).get().first()
            user = user.merge(dbconnection)
            logger.debug("Update user %s after Project save()" % u)
            logger.debug(user)
            db.users(dbconnection, user.dict(), user.id)

        # update slices after Save
        slices = list(set(current['slices']) | set(self.getAttribute('slices')))
        if setup:
            setup.setEndpoints(myslicelibsetup.endpoints)

        for s in current['slices']:
            sl = q(Slice, setup).id(s).get().first()
            db.slices(dbconnection, sl.dict())

        return True

    def delete(self, dbconnection,  setup=None):
        # Get Project from local DB 
        # to update the pi_users after Save
        current = db.get(dbconnection, table='projects', id=self.id)

        result = super(Project, self).delete(setup)
        errors = result['errors']

        if errors:
            raising = True
            for err in errors:
                if "Resolve: Record not found" in err['exception']:
                    raising = False
            if raising:
                raise ProjectException(errors)

        db.delete(dbconnection, 'projects', self.id)

        for u in current['pi_users']:
            user = q(User).id(u).get().first()
            user = user.merge(dbconnection)
            logger.debug("Update user %s after Project delete()" % u)
            logger.debug(user)
            db.users(dbconnection, user.dict(), user.id)

        # Slices will be removed by Sync

        return True
