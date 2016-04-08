##
#   MySlice version 2
#
#   Events thread worker
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##
import logging
from myslice.db.activity import Event, EventStatus, EventAction, Request
from myslice.db import connect, changes, dispatch

logger = logging.getLogger('myslice.service.activity')

def run():
    """
    Manages newly created events
    """
    logger.info("Worker activity events starting")

    # db connection is shared between threads
    dbconnection = connect()

    feed = changes(dbconnection=dbconnection, table='events', filter={ 'status': EventStatus.NEW })
    for ev in feed:

        try:
            event = Event(ev['new_val'])
        except Exception as e:
            logger.error("Problem with event: {}".format(e))
        else:
            if event.action == EventAction.REQ:
                # events that require a request to be created and processes
                logger.info("Received event request from user {}".format(event.user))

                # dispatch a new pending request
                dispatch(dbconnection, Request(event))

                # event status will be set to success
                event.status = EventStatus.SUCCESS

            else:
                # TODO: check userid actually exists
                # TODO: check object id exists
                logger.info("Received event {} from user {}".format(event.action, event.user))
                event.status = EventStatus.WAITING

            # dispatch the updated event
            dispatch(dbconnection, event)