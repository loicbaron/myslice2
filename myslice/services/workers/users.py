##
#   MySlice version 2
#
#   Users thread workers
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##
from pprint import pprint
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

    dbconnection = connect()

    while True:

        try:
            event = Event(qUserEvents.get())
        except Exception as e:
            logger.error("Problem with event: {}".format(e))
        else:
            logger.info("Processing event from user {}".format(event.user))
            with lock:
                try:
                    event.setRunning()
                    isSuccess = False
                    ##
                    # Creating a new user
                    if event.creatingObject():
                        logger.info("Creating user {}".format(event.object.id))
                        user = User()
                        # email
                        user.email = event.data['email']
                        # authority
                        user.authority = event.data['authority']
                        isSuccess = user.save(dbconnection)
                    ##
                    # Deleting user
                    if event.deletingObject():
                        logger.info("Deleting user {}".format(event.object.id))
                        user = User(db.users(dbconnection, id=event.object.id))
                        if not user:
                            raise Exception("User doesn't exist")
                        user.id = event.object.id
                        isSuccess = user.delete(dbconnection)
                    ##
                    # Updating user
                    if event.updatingObject():
                        logger.info("Updating user {}".format(event.object.id))
                        user = User(event.data)
                        user.email = db.users(dbconnection, id=event.object.id)['email']
                        user.id = event.object.id
                        isSuccess = user.save(dbconnection)
                except Exception as e:
                    logger.error("Problem updating user: {} - {}".format(event.object.id, e))
                    event.logError(str(e))
                    event.setError()

                if isSuccess:
                    event.setSuccess()
                else:
                    event.setError()
            ##
            # we then dispatch the event
            db.dispatch(dbconnection, event)

def update_credentials(users):
    # Get users in RethinkDB
    for u_db in db.users():
        # We can only get credentials for users that have a private key stored in db
        if 'private_key' in u_db and u_db['private_key'] is not None:
            for u in users:
                if u.id == u_db['id']:
                    u_db_object = User(u_db)
                    user_setup = UserSetup(u_db_object, myslicelibsetup.endpoints)
                    c = u.getCredentials(setup=user_setup, delegate_to="onelab.myslice")
                    u.private_key = u_db['private_key']
                    u.public_key = u.keys[0]
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
            logger.info("Worker users starting synchronization")

            users = q(User).get()
            users = update_credentials(users)
            """
            update local user table
            """
            if len(users)>0:
                lusers = db.users(dbconnection, users.dict())
            else:
                logger.warning("Query users is empty, check myslicelib and the connection with SFA Registry")

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
