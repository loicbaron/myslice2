from myslicelib.model.user import User as myslicelibUser
from xmlrpc.client import Fault as SFAError

class User(myslicelibUser):

    remote_fields = ['email', 'keys']

    # def isRemoteUpdate(self):
    #     if set(self.attributes()) & set(self.remote_fields):
    #         return True
    #     return False

    def save(self):
        result = super(myslicelibUser, self).save()
        #print(self.attributes())
        #print(result['data'][0])
        if result['errors']:
            if len(result['errors']) == 2 \
                and isinstance(result['errors'][1]['exception'], SFAError) \
                and result['errors'][1]['exception'].faultCode == 7:
                
                return {**(self.attributes()), **result['data'][0]}

            raise Exception('errors: %s' % result['errors'] )
        else:
            return { **(self.attributes()), **result['data'][0]}

    def delete(self):
        result = super(myslicelibUser, self).delete()
        return result if result['errors'] else None


