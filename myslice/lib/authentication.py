import logging

from myslicelib import Setup
from myslicelib.util import Authentication
from myslice import myslicelibsetup

from pprint import pprint

logger = logging.getLogger("myslice-sync")

class UserSetup(Setup):

    def __init__(self, user, endpoints):

        try:
            self._endpoints = endpoints
            # XXX We use the user's certificate and private_key until we are able to delegate credentials to MySlice
            # If the user has no certificate and private_key, it will not work...
            self._authentication = Authentication(hrn=user.hrn, email=user.email, certificate=user.certificate,
                                                       private_key=user.private_key, credentials=user.credentials)
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.error("Problem authenticating with user %s" % user)

class DelegatedSetup(Setup):

    def __init__(self, user, endpoints):

        try:
            self._endpoints = endpoints
            # We use MySlice hrn, email, private_key and certificate
            # We use the user's Credentials delegated to MySlice
            hrn = myslicelibsetup.authentication.hrn
            email = myslicelibsetup.authentication.email
            private_key = myslicelibsetup.authentication.private_key
            certificate = myslicelibsetup.authentication.certificate

            self._authentication = Authentication(hrn=hrn, email=email, certificate=certificate,
                                                       private_key=private_key, credentials=user.credentials)
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.error("Problem authenticating with delegation user %s" % user)
