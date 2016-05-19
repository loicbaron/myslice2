##
#   MySlice version 2
#
#   Users thread workers
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##

import json
import logging
import time
import myslice.db as db
from myslice.lib import Status

from myslice.lib.authentication import UserSetup
from myslice import myslicelibsetup

from myslice.lib.util import format_date

from myslice.db.activity import Event
from myslice.db import connect
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
                
                event.setRunning()
                try:    
                    if event.creatingObject():
                        logger.info("creating the object user {}".format(event.object.id))
                        user = User(event.data)
                        user.id = event.object.id
                        result = user.save()

                    if event.deletingObject():
                        logger.info("delete the object user {}".format(event.object.id))
                        user = User()
                        user.id = event.object.id
                            
                        result = user.delete()
                        # no error , successfuly delted
                        if result is None:
                            db.delete(dbconnection, table='users', id=event.object.id)
                            event.setSuccess()

                    if event.updatingObject():
                        
                        logger.info("updating the user {}".format(event.object.id))
                        user = User(event.data)
                        user.id = event.object.id
                        result = user.save()

                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    logger.error("Problem with event: {}".format(e))
                    result = None
                    event.logError(str(e))
                    event.setError()

                if result:
                    if 'errors' in result and len(result['errors'])>0:
                        logger.error("Error: ".format(result['errors']))
                        event.logError(str(result['errors']))
                        event.setError()
                    else:
                        db.users(dbconnection, result, event.object.id)
                        event.setSuccess()
                
                db.dispatch(dbconnection, event)

def update_credentials(users):
    # Get users in RethinkDB
    for u_db in db.users():
        # We can only get credentials for users that have a private key stored in db
        if 'private_key' in u_db:
            for u in users:
                u_db_object = User(u_db)
                if u.id == u_db['id']:
                    user_setup = UserSetup(u_db_object, myslicelibsetup.endpoints)

                    # XXX the admin user hrn must be a setting
                    c = u.getCredentials(setup=user_setup, delegate_to="onelab.myslice")
    return users

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
            users = update_credentials(users)
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
