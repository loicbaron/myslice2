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

def run(c):
    """

    """
    logger.info("Worker activity events starting")

    feed = changes(c=c, table='events', filter={ 'status': EventStatus.NEW })
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
                req.save()

                # change the status of the event to waiting
                ev.status = EventStatus.WAITING
                ev.dispatch()
            else:
                # all other types of requests
                pass
