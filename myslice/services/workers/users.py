##
#   MySlice version 2
#
#   Users thread workers
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##

import logging
import time
import myslice.db as db
from myslice.lib import Status
from myslice.lib.util import format_date

from myslice.db.activity import Event, EventAction, EventStatus, Object, ObjectType 
from myslice.db import changes, connect
from myslice.db.user import User
from myslicelib.query import q

logger = logging.getLogger('myslice.service.users')


def events_run(lock, qUserEvents):
    """
    Process the user after approval 
    """

    logger.info("Worker users events starting") 

    # db connection is shared between threads
    dbconnection = connect()

    while True:

        try:
            event = Event(qUserEvents.get())
        except Exception as e:
            logger.error("Problem with event: {}".format(e))
        finally:
            logger.info("Processing event from user {}".format(event.user))
            
            with lock:
                try:
                    event.setRunning()
                    
                    # TODO: CREATE & DELETE
                    if event.creatingObject():
                    

                    # if event.deletingObject():

                    if event.updatingObject():
                        result = event.data

                    if event.addingObject():

                        user = User(db.get(dbconnection, table='users', id=event.object.id))
                        
                        if event.data['type'] == 'KEY':
                            user.addKey(event.data['key'])
                            result = user.save()

                    if event.removingObject():

                        user = User(db.get(dbconnection, table='users', id=event.object.id))
                        
                        if event.data['type'] == 'KEY':
                            user.delKey(event.data['key'])
                            result = user.save()

                except Exception as e:
                    logger.error("Problem with event: {}".format(e))
                    result = None
                    event.logError(str(e))
                    event.setError()
                     
                if result:
                    print(result)
                    db.users(dbconnection, result, event.user)
                    event.setSuccess()
                
                db.dispatch(dbconnection, event)

def sync(lock):
    """
    A thread that will sync users with the local rethinkdb
    """

    # DB connection
    dbconnection = db.connect()

    while True:
        # acquires lock
        with lock:
            logger.info("Worker users starting period synchronization")

            users = q(User).get()

            """
            update local user table
            """
            lusers = db.users(dbconnection, users.dict())

            for ls in lusers :
                # add status if not present and update on db
                if not 'status' in ls:
                    ls['status'] = Status.ENABLED
                    ls['enabled'] = format_date()
                    db.users(dbconnection, ls)

                if not users.has(ls['id']) and ls['status'] is not Status.PENDING:
                    # delete resourc that have been deleted elsewhere
                    db.delete(dbconnection, 'users', ls['id'])
                    logger.info("User {} deleted".format(ls['id']))

 

            logger.info("Worker users finished period synchronization") 
        
        # sleep
        time.sleep(86400)
