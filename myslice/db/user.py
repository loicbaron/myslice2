from myslicelib.model.user import User as myslicelibUser
from xmlrpc.client import Fault as SFAError

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

    remote_fields = ['email', 'keys']
    private_key = None
    public_key = None
    generate_keys = False

    # def isRemoteUpdate(self):
    #     if set(self.attributes()) & set(self.remote_fields):
    #         return True
    #     return False

    def save(self):
        if self.generate_keys:
            private_key, public_key = generate_RSA()
            self.private_key = private_key.decode('utf-8')
            self.public_key = public_key.decode('utf-8')
            self.keys.append(self.public_key)

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
        
        if result['errors']:
            raise Exception('errors: %s' % result['errors'])
        return None


