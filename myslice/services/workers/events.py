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
            if event.creatingObject():
                # events that require a request to be created and processes
                logger.info("Received event request from user {}".format(event.user))
                event.setPending()
            # TODO: check that 
            # user has the rights to do the action -> waiting
            # Check in local DB 
            #    Slice -> if user in users
            #    Authority & Project -> if event.user in pi_users of event.object.id or an upper authority
            #    User -> if event.user == event.object.id
            #            or if event.user in pi_users of authority of event.object.id or an upper authority
            #
            # event.setWaiting()
            else:
                # TODO: check userid actually exists
                # TODO: check object id exists
                logger.info("Received event {} from user {}".format(event.action, event.user))
                # event will wait to be processed by the appropriate service
                event.setWaiting()

            # dispatch the updated event
            dispatch(dbconnection, event)
