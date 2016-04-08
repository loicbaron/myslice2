##
#   MySlice version 2
#
#   Events thread workers
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##

import pprint
import logging
from myslice.db.model import Event, EventStatus, EventAction, Request, RequestStatus
from myslice.db import changes

logger = logging.getLogger('myslice.service.activity')

def run(dbconnection):
    """

    """
    logger.info("Worker activity events starting")

    feed = changes(c=dbconnection, table='events', filter={ 'status': EventStatus.NEW })
    for event in feed:
        print(event)
        try:
            ev = Event(event['new_val'])
        except Exception as e:
            logger.error("Problem with event: {}".format(e))
        finally:
            if ev.action == EventAction.REQ:
                # events that require a request to be created and processes
                logger.info("Received event request from user {}".format(ev.user))

                # creates new pending request
                req = Request({
                    'user': ev.user,
                    'event': ev.id,
                    'status': RequestStatus.PENDING
                })
                req.dispatch(dbconnection)

                # event status will be set to success
                ev.status = EventStatus.SUCCESS
                ev.dispatch()
            else:
                # TODO: check userid actually exists
                # TODO: check object id exists
                ev.status = EventStatus.WAITING
                ev.dispatch()