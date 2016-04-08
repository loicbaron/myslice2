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

def run():
    """
    Processes requests
    """
    logger.info("Worker activity requests starting")

    # db connection is shared between threads
    dbconnection = connect()

    feed = changes(dbconnection=dbconnection, table='requests', filter={ 'status': RequestStatus.PENDING })
    for req in feed:

        try:
            request = Request(req['new_val'])
        except Exception as e:
            logger.error("Problem with request: {}".format(e))
        finally:
            logger.info("Processing request from user {}".format(req.user))

            # get the user
            #user = q(User).id(request.user).get()

            if request.status == RequestStatus.PENDING:
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


            elif request.status == RequestStatus.APPROVED:
                pass

