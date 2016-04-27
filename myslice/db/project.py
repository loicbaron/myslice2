from myslicelib.model.project import Project as myslicelibProject
from myslice.db.activity import Object, ObjectType
from xmlrpc.client import Fault as SFAError

class Project(myslicelibProject):

    def save(self):
        result = super(myslicelibProject, self).save()

        if result['errors']:
            if len(result['errors']) == 2 \
                and isinstance(result['errors'][1]['exception'], SFAError) \
                and result['errors'][1]['exception'].faultCode == 7:
                
                return result['data']

            raise Exception('errors: %s' % result['errors'] )
        else:
            return result['data']



