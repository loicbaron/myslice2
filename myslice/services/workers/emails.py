##
#   MySlice version 2
#
#   Events thread worker
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##
import logging
from myslice.db.activity import Event
from myslice.db import connect, dispatch

logger = logging.getLogger('myslice.service.activity')

def run(q):
    """
    Manages newly created events
    """
    logger.info("Worker activity events starting")

    # db connection is shared between threads
    dbconnection = connect()

    while True:
        try:
            event = Event(q.get())
        except Exception as e:
            logger.error("Problem with event: {}".format(e))
        else:
            if event.isPending():
                # send email to PIs
                # Get PIs for the authority responsible of the Object
                logger.info("Send email Request Pending to  PIs {}".format(event.user))
            elif event.isDenied():
                # send email to User
                logger.info("Send email Request Denied to  user {}".format(event.user))
            elif event.isApproved():
                # send email to User
                logger.info("Send email Request Approved to  user {}".format(event.user))
