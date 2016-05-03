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

logger = logging.getLogger('myslice.service.activity')

def check_user_rights(user, event):
    if event.object.type == ObjectType.SLICE:
        for s in user.slices:
            if s == event.object.id:
                return True
    elif event.user == event.object.id:
        return True
    else:
        for a in user.pi_authorities:
            if event.object.id.split('+')[1].startswith(a.split('+')[1]):
                return True
    return False

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
                db_user = db.get(dbconnection, table='users', id=event.user)
                print(event)
                if db_user:
                    user = User(db_user)
                    if check_user_rights(user,event):
                        event.setWaiting()
                    else:
                        event.setPending()
                else:
                    event.setError()
                    logger.error("User %s not found" % event.user)
                    # raising an Exception here, blocks the REST API
                    #raise Exception("User %s not found" % event.user)
            except Exception as e:
                event.setError()
                logger.error("Unable to fetch the user from db {}".format(e))

            # dispatch the updated event
            dispatch(dbconnection, event)
