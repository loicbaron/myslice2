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

class UserException(Exception):
    def __init__(self, errors):
        self.stack = errors

class User(myslicelibUser):
    
    def __init__(self, data = {}):
        data = data if data is not None else {}
        data['generate_keys'] = data.get('generate_keys', False)
        data['private_key'] = data.get('private_key', None)
        data['public_key'] = data.get('public_key', None)
        data['keys'] = data.get('keys', [])
        data['credentials'] = data.get('credentials', [])
        super(User, self).__init__(data)

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
        if self.getAttribute('id') == event.object.id:
            return True

        if event.object.type == ObjectType.SLICE and event.object.id in self.getAttribute('slices'):
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
        if self.getAttribute('generate_keys'):
            private_key, public_key = generate_RSA()
            self.setAttribute('private_key', private_key.decode('utf-8'))
            self.setAttribute('public_key', public_key.decode('utf-8'))
            self.appendAttribute('keys', self.getAttribute('public_key'))

        result = super(User, self).save(setup)
        errors = result['errors']

        result = { **(self.dict()), **result['data'][0]}
        # add status if not present and update on db
        if not 'status' in result:
            result['status'] = Status.ENABLED
            result['enabled'] = format_date()

        db.users(dbconnection, result, self.getAttribute('id'))
        if errors:
            raise UserException(errors)
        else:
            return True

    def delete(self, dbconnection, setup=None):
        result = super(User, self).delete(setup)
        errors = result['errors']
        
        db.delete(dbconnection, 'users', self.getAttribute('id'))

        if errors:
            raise UserException(errors)
        else:
            return True


