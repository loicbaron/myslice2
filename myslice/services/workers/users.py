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
            print(event)
        except Exception as e:
            logger.error("Problem with event: {}".format(e))
        finally:
            logger.info("Processing event from user {}".format(event.user))
            
            with lock:
                
                event.setRunning()
                try:    
                    if event.creatingObject():
                        logger.info("creating the user {}".format(event.object.id))
                        user = User(event.data)
                        user.id = event.object.id
                        result = user.save()

                    if event.deletingObject():
                        logger.info("delete the object to user {}".format(event.object.id))
                        user = User()
                        user.id = event.object.id
                            
                        result = user.delete()
                        db.delete(dbconnection, table='users', id=event.object.id)
                        event.setSuccess()

                    if event.updatingObject():
                        
                        # if user.isRemoteUpdate():
                        #     logger.info("updating remotely the user {}".format(event.object.id))
                        #     user.id = event.object.id
                        #     # update both remote fileds and local fields(if exists)                           
                        #     result = event.data.update(user.save().first().dict())
                        # else:
                        #     logger.info("updating locally the user {}".format(event.object.id))
                        #     result = event.data

                        logger.info("updating the user {}".format(event.object.id))
                        user = User(event.data)
                        user.id = event.object.id
                        result = user.save()

                    # if event.addingObject():
                    #     logger.info("adding the object to user {}".format(event.object.id))

                    #     user = User(db.get(dbconnection, table='users', id=event.object.id))                        
                        
                    #     if event.data['type'] == 'KEY':
                    #         user.addKey(event.data['value'])
                    #         result = user.save()

                    # if event.removingObject():
                    #     logger.info("remove the object from user {}".format(event.object.id))

                    #     user = User(db.get(dbconnection, table='users', id=event.object.id))
                    #     if event.data['type'] == 'KEY':
                    #         user.delKey(event.data['value'])
                    #         result = user.save()

                except Exception as e:
                    logger.error("Problem with event: {}".format(e))
                    result = None
                    event.logError(str(e))
                    event.setError()
                     
                if result:
                    print(result)
                    logger.info("Success with event from user {}".format(event.user))
                    db.users(dbconnection, result, event.object.id)
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
