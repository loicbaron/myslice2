import logging

from myslicelib.model.user import User as myslicelibUser
from xmlrpc.client import Fault as SFAError
from myslice import db
from myslice.db.activity import ObjectType
from myslice.lib import Status
from myslice.lib.util import format_date

logger = logging.getLogger('myslice.db.user')

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
        # Generate keys by default
        data['generate_keys'] = data.get('generate_keys', True)
        data['private_key'] = data.get('private_key', None)
        data['public_key'] = data.get('public_key', None)
        data['keys'] = data.get('keys', [])
        data['credentials'] = data.get('credentials', [])
        data['terms'] = data.get('terms', 'on')
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
        if self.getAttribute('id') == event.object.id:
            return True

        # user updates its own slices(experiments)
        if event.object.type == ObjectType.SLICE and event.object.id in self.getAttribute('slices'):
            return True

        # user updates leases in its own slices(experiments)
        if event.object.type == ObjectType.LEASE:
            if isinstance(event.data, list):
                if event.data[0]['slice_id'] in self.getAttribute('slices'):
                    return True
            elif event.data['slice_id'] in self.getAttribute('slices'):
                return True

        if event.object.type != ObjectType.LEASE:
            # user is Pi of the obj he wants to update
            for auth in self.getPiAuthorities(attribute=True):
                ev_auth = event.data.get('authority', event.object.id)
                if ev_auth:
                    if auth == ev_auth:
                        return True
                    if get_header(ev_auth).startswith(get_header(auth)):
                        return True
                if auth == event.object.id:
                    return True

        return False

    def isAdmin(self):
        auth_pattern = re.compile(r"(urn:publicid:IDN\+)(?P<hrn>[\:]*[a-zA-Z]*)(\+authority\+sa)")
        flag = False
        try:
            # XXX not sure if it is a clean way to decide a admin
            pi_auth = self.get('pi_authorities')
            for auth in pi_auth:
                m = auth_pattern.match(auth)
                # User has only Projects and No Authorities under pi_authorities
                if m is None:
                    logger.debug("%s does not match regex" % auth)
                    flag = False
                else:
                    hrn_length = len(m.group('hrn').split(':'))
                    if hrn_length == 1:
                        return True
            return flag
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.serverError("unable to identify user permission")
            return False

    # This functions keeps the locally stored private/public keys of the user
    def merge(self, dbconnection):
        db_user = db.get(dbconnection, table='users', id=self.id)
        if db_user:
            if 'private_key' in db_user:
                self.setAttribute('private_key', db_user['private_key'])
            if 'public_key' in db_user:
                self.setAttribute('public_key', db_user['public_key'])
            if 'password' in db_user:
                self.setAttribute('password', db_user['password'])
            if 'generate_keys' in db_user:
                self.setAttribute('generate_keys', db_user['generate_keys'])

        return self

    def save(self, dbconnection, setup=None):
        logger.warning("User.save() called")
        # Get User from local DB 
        current = db.get(dbconnection, table='users', id=self.id)

        if self.getAttribute('generate_keys'):
            private_key, public_key = generate_RSA()
            self.setAttribute('private_key', private_key.decode('utf-8'))
            self.setAttribute('public_key', public_key.decode('utf-8'))
            self.appendAttribute('keys', self.getAttribute('public_key'))
            # Once it is generated, turn this option off
            self.setAttribute('generate_keys', False)

        result = super(User, self).save(setup)
        errors = result['errors']
        # Raise exception to send the errors as logs
        if errors:
            raise UserException(errors)

        result = { **(self.dict()), **result['data'][0]}
        # add status if not present and update on db
        if not 'status' in result:
            result['status'] = Status.ENABLED
            result['enabled'] = format_date()
        # Update user in local DB
        if not self.getAttribute('id'):
            raise UserException("This user has no id, could not be saved in local DB: {}".format(self))
        logger.debug("DB user save()")
        logger.debug(result)
        if not self.getAttribute('id'):
            logger.critical("-------> USER HAS NO ID <-------")
            raise Exception("Trying to save a user that has no id will remove all data in users table!!!")
        # New User created
        if current is None:
            db.users(dbconnection, result)
        else:
            db.users(dbconnection, result, self.getAttribute('id'))
        return True

    def delete(self, dbconnection, setup=None):
        logger.warning("User.delete() called")
        logger.debug(self.getAttribute('id'))
        result = super(User, self).delete(setup)
        errors = result['errors']
        if errors:
            raising = True
            for err in errors:
                if "Record not found" in err['exception']:
                    raising = False
                    break
            if raising:
                raise UserException(errors)

        db.delete(dbconnection, 'users', self.getAttribute('id'))

        return True


