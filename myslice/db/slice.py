from myslicelib.model.slice import Slice as myslicelibSlice
from myslicelib.query import q
from myslice.db.activity import Object, ObjectType
from myslice import db
from myslice.db.user import User
from myslice.lib import Status
from myslice.lib.util import format_date
from xmlrpc.client import Fault as SFAError

class SliceException(Exception):
    def __init__(self, errors):
        self.stack = errors

class Slice(myslicelibSlice):

    def save(self, dbconnection, setup=None):
        result = super(Slice, self).save(setup)
        errors = result['errors']

        result = {**(self.dict()), **result['data'][0]}
        # add status if not present and update on db
        if not 'status' in result:
            result['status'] = Status.ENABLED
            result['enabled'] = format_date()

        db.slices(dbconnection, result, self.id)

        # Get Slice from local DB 
        # to update the users after Save
        current = db.get(dbconnection, table='slices', id=self.id)
        for user in current['users']:
            db.users(dbconnection, q(User).id(user).get().dict())

        if errors:
            raise SliceException(errors)
        else:
            return True

    def delete(self, dbconnection, setup=None):
        result = super(Slice, self).delete(setup)
        errors = result['errors']

        db.delete(dbconnection, 'slices', self.id)

        # Get Slice from local DB 
        # to update the users after Save
        current = db.get(dbconnection, table='slices', id=self.id)
        for user in current['users']:
            db.users(dbconnection, q(User).id(user).get().dict())

        if errors:
            raise SliceException(errors)
        else:
            return True
