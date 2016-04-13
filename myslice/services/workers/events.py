##
#   MySlice version 2
#
#   Events thread worker
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##
import logging
from myslice.db.activity import Event, EventStatus, EventAction
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
            if event.status == EventStatus.NEW and event.action == EventAction.REQ:
                # events that require a request to be created and processes
                logger.info("Received event request from user {}".format(event.user))

                # event is of type request, we put it on PENDING
                event.status = EventStatus.PENDING

            elif event.status == EventStatus.NEW:
                # TODO: check userid actually exists
                # TODO: check object id exists
                logger.info("Received event {} from user {}".format(event.action, event.user))
                event.status = EventStatus.WAITING

            # dispatch the updated event
            dispatch(dbconnection, event)