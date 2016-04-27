from myslicelib.model.slice import Slice as myslicelibSlice
from xmlrpc.client import Fault as SFAError

class Slice(myslicelibSlice):

    def save(self):
        result = super(myslicelibSlice, self).save()
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
        result = super(myslicelibSlice, self).delete()
        
        if result['errors']:
            raise Exception('errors: %s' % result['errors'])
        return None


