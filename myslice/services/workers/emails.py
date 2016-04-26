##
#   MySlice version 2
#
#   Requests thread workers
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##

import logging
import time

from myslice.db.activity import Event 
from myslice.db import changes, connect
from myslice.db.user import User
#from myslice.db.email import Email

logger = logging.getLogger('myslice.service.emails')


def run(qEmails):
    """
    Process emails
    """

    logger.info("Worker emails starting") 

    # db connection is shared between threads
    dbconnection = connect()

    while True:
        try:

            event = Event(qEmails.get())

        except Exception as e:
            logger.error("Problem with event: {}".format(e))
        else:
            if event.isPending():
                print('here')
                e = Email(event)
                e.compose().send()
            elif event.isDenied():
                pass
            elif event.isApproved:
                pass
