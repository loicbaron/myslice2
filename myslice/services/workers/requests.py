##
#   MySlice version 2
#
#   Requests thread workers
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##

import logging
from myslice.db.activity import Request, RequestStatus
from myslice.db import connect, changes
from myslicelib.model.user import User
from myslicelib.query import q

logger = logging.getLogger('myslice.service.activity')

def run(q):
    """
    Processes requests
    """
    logger.info("Worker activity requests starting")

    while True:
        try:
            request = Request(q.get())
        except Exception as e:
            logger.error("Problem with request: {}".format(e))
        finally:
            logger.info("Processing request from user {}".format(request.user))

            # get the user
            #user = q(User).id(request.user).get()

            if request.status == RequestStatus.PENDING:
                ##
                # Request is pending, is user is already a PI
                # we set the statuso to APPROVED, else we wait
                # for a PI to validate

                print(request)
                # retrieve the event
                #ev = Event(event(req.event))

                #
                # IF request is for a new project
                # project = Project({'hrn':req.object.name})
                # authority = Authority({'hrn':project.authority})
                # authority.getPi_users()
                #
                # project.getAuthority().isPi(user)
                #
                # ##
                # # slice
                # project.isPi(user)
                # # if user is pi we approve the request
                # if project.authority.isPi():
                #     req.approve()