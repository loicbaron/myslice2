import logging

from myslicelib import Setup
from myslicelib.util import Authentication

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