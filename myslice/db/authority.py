from myslicelib.model.authority import Authority as myslicelibAuthority
from myslice.db.activity import Object, ObjectType
from xmlrpc.client import Fault as SFAError

class Authority(myslicelibAuthority):

    def save(self, setup=None):
        result = super(myslicelibAuthority, self).save(setup)

        if result['errors']:
            if len(result['errors']) == 2 \
                and isinstance(result['errors'][1]['exception'], SFAError) \
                and result['errors'][1]['exception'].faultCode == 7:
                
                return result['data']

            raise Exception('errors: %s' % result['errors'] )
        else:
            return result['data']



