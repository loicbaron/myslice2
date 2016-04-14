from myslicelib.model.user import User as myslicelibUser
from myslice.db.activity import Object, ObjectType
from xmlrpc.client import Fault as SFAError

class User(myslicelibUser):

    def __init__(self, data = None):
        super().__init__(data)
        if data is None:
            self.keys = []

    # def isPi(self, obj):
    #     if obj.type == ObjectType.User:
    #         return obj.id == self.id
        
    #     if obj.type == ObjectType.SLICE:
    #         return obj.id in self.slices

    #     if obj.type == ObjectType.PROJECT:
    #         return obj.id in self.pi_authorities

    #     raise NotImplementedError('User isPi method dont support current obj type')

    def addKey(self, key):
        if key in self.keys:
            raise Exception('Same key already exists') 
        else:
            # Adding key to the left of list is beacause 
            # SFA check the keys from left to right
            # only keys in the front of list can raise a key convert in 

            self.keys.append(key)
            return self

    def delKey(self, key):
        if key not in self.keys:
            raise Exception("Cannot delete a key doesn't exists")
        else:
            self.keys.remove(key)
            return self

    # def save(self):
    #     result = super(myslicelibUser, self).save()

    #     print("===========wired ========")
    #     print(result)
        # if result['errors']:
        #     print(result['errors'])
        #     if len(result['errors']) == 2 \
        #         and isinstance(result['errors'][0]['exception'], SFAError) \
        #         and result['errors'][0]['exception'].faultCode == 7:
                
        #         return result['data']

        #     raise Exception('errors: %s' % result['errors'] )
        # else:
        #     return result['data']
