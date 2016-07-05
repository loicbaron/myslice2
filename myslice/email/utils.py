import os
from random import randrange
from datetime import datetime

from myslice.settings import s

DOMAIN = s.email.domain

class MessageID:
    """Returns a string suitable for RFC 2822 compliant Message-ID, e.g:
    <20020201195627.33539.96671@mx.google.com>
    Optional idstring if given is a string used to strengthen the
    uniqueness of the message id.

    """

    def __init__(self, idstring=None):
        self.domain = DOMAIN
        try:
            pid = os.getpid()
        except AttributeError:
            # No getpid() in Jython.
            pid = 1
        self.idstring = ".".join([str(idstring or randrange(10000)), str(pid)])

    def __call__(self):
        r = ".".join([datetime.now().strftime("%Y%m%d%H%M%S.%f"),
                      str(randrange(100000)),
                      self.idstring])
        return "".join(['<', r, '@', self.domain, '>'])