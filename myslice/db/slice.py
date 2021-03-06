import logging
from pprint import pprint

from myslicelib.model.slice import Slice as myslicelibSlice
from myslicelib.query import q
from myslice.db.activity import Object, ObjectType
from myslice import db
from myslice.db.user import User
from myslice.lib import Status
from myslice.lib.util import format_date
from xmlrpc.client import Fault as SFAError

logger = logging.getLogger('myslice.db.slice')

class SliceException(Exception):
    def __init__(self, errors):
        self.stack = errors

class SliceWarningException(Exception):
    def __init__(self, errors):
        self.stack = errors

class Slice(myslicelibSlice):

    def __init__(self, data = {}):
        # initialize the object with its id
        if isinstance(data, str):
            data = db.slices(id=data)

        data = data if data is not None else {}
        data['hasLeases'] = False
        if 'leases' in data and len(data['leases'])>0:
            data['hasLeases'] = True
        data['removedLeases'] = []
        super(Slice, self).__init__(data)

    def save(self, dbconnection, setup=None):
        # Get Slice from local DB 
        # to update the users after Save
        current = db.get(dbconnection, table='slices', id=self.id)

        result = super(Slice, self).save(setup)
        errors = result['errors']
        result = {**(self.dict()), **result['data'][0]}
        if not errors:
            for r in result['resources']:
                if (not 'services' in r) or (not r['services']):
                    logger.warning("result from slice.save didn't had login info")
                    logger.warning("sleeping 10s before asking again to AMs")
                    import time
                    time.sleep(10)
                    slice = q(Slice, setup).id(self.id).get().first()
                    result = slice.dict()
                    break
        # add status if not present and update on db
        if not 'status' in result:
            result['status'] = Status.ENABLED
            result['enabled'] = format_date()

        # New Slice created
        if current is None:
            db.slices(dbconnection, result)
            current = db.get(dbconnection, table='slices', id=self.id)
        # Update existing slice
        else:
            db.slices(dbconnection, result, self.id)

        # Update users both previously and currently in Slice
        users = list(set(current['users']) | set(self.getAttribute('users')))
        for u in users:
            user = q(User).id(u).get().first()
            if user:
                user = user.merge(dbconnection)
                logger.debug("Update user %s after Slice save()" % u)
                logger.debug(user)
                user = user.dict()
            else:
                logger.error("Could not update user after Slice.save(), no answer from Registry")
                logger.warning("Updating the local DB manually")
                user = db.get(dbconnection, table='users', id=u)
                if u in current['users'] and u not in self.getAttribute('users'):
                    # Remove slice from user
                    del u['slices'][self.id]
                elif u not in current['users'] and u in self.getAttribute('users'):
                    # Add slice to user
                    u['slice'].append(self.id)

            db.users(dbconnection, user, u)

        # Update the Project of the slice
        logger.debug("cooko slice: {}".format(self))
        project = db.get(dbconnection, table='projects', id=self.project)
        project['slices'] = project['slices'] + [self.id]
        db.projects(dbconnection, project)

        # Insert / Delete Leases if necessary
        if self.hasLeases:
            flag = -1
            for lease in self.leases:
                # No resources reserved
                if len(result['leases'])==0:
                    flag = -1
                # All resources of a Lease have been succesfully reserved
                elif lease['resources'] == result['leases'][0]['resources']:
                    flag = 0
                # Some Resources of a Lease have been reserved
                elif len(set(lease['resources']).intersection(set(result['leases'][0]['resources']))) > 0:
                    db.leases(dbconnection, lease)
                    flag = 1
            for lease in self.removedLeases:
                if lease not in result['leases']:
                    db.delete(dbconnection, 'leases', lease.id)
                    flag = False
            if flag == -1:
                errors.append("No reservation has been accepted by the testbeds")
            elif flag == 1:
                errors.append("Some resources have been reserved others were unavailable")
                raise SliceWarningException(errors)

        if errors:
            raise SliceException(errors)
        else:
            return True

    def delete(self, dbconnection, setup=None):
        # Get Slice from local DB 
        # to update the users after Save
        current = db.get(dbconnection, table='slices', id=self.id)

        result = super(Slice, self).delete(setup)
        errors = result['errors']

        # Signal only Registry Errors
        if errors:
            raising = False
            for err in errors:
                if err['type'] == "Reg":
                    if "Record not found" in err['exception']:
                        raising = False
                    else:
                        raising = True
            if raising:
                raise SliceException(errors)

        db.delete(dbconnection, 'slices', self.id)

        for u in current['users']:
            user = q(User).id(u).get().first()
            if user:
                user = user.merge(dbconnection)
                logger.debug("Update user %s after Slice delete()" % u)
                logger.debug(user)
                user = user.dict()
            else:
                logger.error("Could not update user after Slice.delete(), no answer from Registry")
                logger.warning("Updating the local DB manually")
                user = db.get(dbconnection, table='users', id=u)
                # Remove slice from user
                del u['slices'][self.id]

            db.users(dbconnection, user, u)

        # Update the Project of the slice
        project = db.get(dbconnection, table='projects', id=self.project)
        project['slices'] = list(set(project['slices']) - set([self.id]))
        db.projects(dbconnection, project)

        # Warning if errors on AMs
        #if errors:
        #    raise SliceWarningException(errors)

        return True

    def addLease(self, lease):
        self = super(Slice, self).addLease(lease)
        self.hasLeases = True

    def removeLease(self, lease):
        self = super(Slice, self).removeLease(lease)
        self.hasLeases = True
        self.removedLeases.append(lease.id)
