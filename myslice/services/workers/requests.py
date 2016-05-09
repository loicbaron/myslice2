##
#   MySlice version 2
#
#   Requests thread workers
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##

import logging
from myslice.db import connect, users
from myslice.db.activity import Event 
from myslice.db.message import PortalMessage
from myslice.db.message import Mailer
from myslice import settings as s


logger = logging.getLogger('myslice.service.requests')


def run(qRequests):
    """
    Process Requests and send Emails accordingly
    """

    logger.info("Worker Requests starting") 

    # db connection is shared between threads
    dbconnection = connect()

    while True:
        try:
            event = Event(qRequests.get())
        except Exception as e:
            logger.error("Problem with event: {}".format(e))
        else:
            user = db.user
