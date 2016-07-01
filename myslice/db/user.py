from myslicelib.model.user import User as myslicelibUser
from xmlrpc.client import Fault as SFAError
from myslice import db
from myslice.db.activity import ObjectType
from myslice.lib import Status
from myslice.lib.util import format_date
from pprint import pprint

def generate_RSA(bits=2048):
    '''
    Generate an RSA keypair with an exponent of 65537 in PEM format
    param: bits The key length in bits
    Return private key and public key
    '''
    try:
        from Crypto.PublicKey import RSA
        new_key = RSA.generate(bits)

        # Example: private_key = '-----BEGIN RSA PRIVATE KEY-----\nMIIC...'
        # Example: public_key = 'ssh-rsa AAAAB3...'
        private_key = new_key.exportKey()
        public_key  = new_key.publickey().exportKey(format='OpenSSH')
    except Exception as e:
        import traceback
        traceback.print_exc()
    return private_key, public_key

class User(myslicelibUser):
    
    def __init__(self, data = {}):
        super(User, self).__init__(data)
        if data is None:
            data = {}
        self.generate_keys = data.get('generate_keys', False)
        self.keys = data.get('keys', [])
        self.credentials = data.get('credentials', [])
        self.hashing = data.get('hashing', '')

    def has_privilege(self, event):
        '''
        Return True if user has the privlege over the object.
        '''
        def get_header(string):
            '''
            Return the header of urn in order to check privilege
            '''
            return string.split('+authority')[0]

        # user updates its own property
        # user updates its own slices(experiments)
        # user is Pi of the obj he wants to update
        if self.id == event.object.id:
            return True

        if event.object.type == ObjectType.SLICE and event.object.id in self.slices:
            return True

        for auth in self.getPiAuthorities(attribute=True):
            ev_auth = event.data.get('authority', [])
            if ev_auth:
                if auth == ev_auth:
                    return True
                if get_header(ev_auth).startswith(get_header(auth)):
                    return True
            if auth == event.object.id:
                return True

        return False

    def save(self, dbconnection, setup=None):
        if self.generate_keys:
            private_key, public_key = generate_RSA()
            self.private_key = private_key.decode('utf-8')
            self.public_key = public_key.decode('utf-8')
            self.keys.append(self.public_key)

        result = super(User, self).save(setup)

        if result['errors']:
            raise Exception('errors: %s' % result['errors'] )
        else:
            result = { **(self.dict()), **result['data'][0]}
            # add status if not present and update on db
            if not 'status' in result:
                result['status'] = Status.ENABLED
                result['enabled'] = format_date()

            db.users(dbconnection, result, self.id)
            return True

    def delete(self, dbconnection, setup=None):
        result = super(User, self).delete(setup)
        
        if result['errors']:
            raise Exception('errors: %s' % result['errors'])
        else:
            db.delete(dbconnection, 'users', self.id)
            return True


