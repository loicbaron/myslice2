##
#   MySlice version 2
#
#   Events thread worker
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##
import logging
import time
from pprint import pprint
import myslice.db as db
from myslice.db import connect, dispatch
from myslice.db.activity import Event, ObjectType 
from myslice.db.user import User
from myslice.lib.sfa import has_privilege

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
            event.setError()
            logger.error("Problem with event: {}".format(e))
        else:
            try:

                # TODO: if event.creatingObject() 
                # Check if the event.object.id already exists or not
                # if it exists -> add a numer to the id & hrn to make it unique

                # Register a new user
                if event.user is None:
                    if event.creatingObject():
                        event.setPending()
                    else:
                        raise Exception('User must be specified unless creating Object')
                else:
                    db_user = db.get(dbconnection, table='users', id=event.user)  
                    if not db_user:
                        raise Exception("User %s not found" % event.user)
                    
                    user = User(db_user)
                    if has_privilege(user, event.object):
                        event.setWaiting()
                    else:
                        event.setPending()

            except Exception as e:
                event.setError()
                event.logError(str(e))
                logger.error("Unable to fetch the user from db {}".format(e))

            # dispatch the updated event
            dispatch(dbconnection, event)
