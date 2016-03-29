##
#   MySlice version 2
#
#   Requests thread workers
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##

import pprint
import logging
from myslice.db.model import Event, EventStatus, EventAction, Request, RequestStatus
from myslice.db import changes, event
from myslicelib.model.user import User
from myslicelib.query import q

logger = logging.getLogger('myslice.service.activity')

def run(c):
    """
    Processes requests
    """
    logger.info("Worker activity requests starting")

    feed = changes(c=c, table='requests', filter={ 'status': RequestStatus.PENDING })
    for request in feed:
        print(request)
        try:
            req = Request(request['new_val'])
        except Exception as e:
            logger.error("Problem with request: {}".format(e))
        finally:
            logger.info("Processing request from user {}".format(req.user))

            # get the user
            user = q(User).id(req.user).get()

            # retrieve the event
            ev = Event(event(req.event))

            # if user is pi
            if user.isPi():
                req.approve()
                ev.status = EventStatus.SUCCESS
                ev.dispatch()
            else:
                pass

