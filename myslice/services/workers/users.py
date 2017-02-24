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
            event.logError(str(e))
            event.setError()
            dispatch(dbconnection, event)
        else:
            logger.info("Processing event from user {}".format(event.user))
            with lock:
                try:
                    event.setRunning()
                    isSuccess = False

                    # If we generate a new key pair the Query will not work, use the myslice account for that
                    if event.user and hasattr(event.object, 'generate_keys') and event.object.generate_keys is False:
                        u = User(db.get(dbconnection, table='users', id=event.user))
                        user_setup = UserSetup(u, myslicelibsetup.endpoints)
                    else:
                        user_setup = None
                    ##
                    # Creating a new user
                    if event.creatingObject():
                        logger.info("Creating user {}".format(event.object.id))
                        user = User(event.data)
                        isSuccess = user.save(dbconnection, user_setup)
                    ##
                    # Deleting user
                    if event.deletingObject():
                        logger.info("Deleting user {}".format(event.object.id))
                        user = User(db.users(dbconnection, id=event.object.id))
                        if not user:
                            raise Exception("User doesn't exist")
                        user.id = event.object.id
                        isSuccess = user.delete(dbconnection, user_setup)
                    ##
                    # Updating user
                    if event.updatingObject():
                        logger.info("Updating user {}".format(event.object.id))
                        user = User(event.data)
                        user.email = User(db.users(dbconnection, id=event.object.id)).email
                        user.id = event.object.id
                        isSuccess = user.save(dbconnection, user_setup)
                except Exception as e:
                    import traceback
                    traceback.print_exc()
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

def update_credentials(user):
    # We can only get credentials for users that have a private key stored in db
    if 'private_key' in user and user['private_key'] is not None:
        u = User(user)
        user_setup = UserSetup(u, myslicelibsetup.endpoints)
        if u.hrn == "onelab.myslice":
            c = u.getCredentials(setup=user_setup)
        else:
            c = u.getCredentials(setup=user_setup, delegate_to="onelab.myslice")
        u.private_key = user['private_key']
        u.public_key = u.keys[0]
        return u.dict()
    return user

def sync(lock, email=None, job=True):
    """
    A thread that will sync users with the local rethinkdb
    """

    if job:
        while True:
            syncUsers(lock, email)

            # sleep
            time.sleep(3600)
    else:
        syncUsers(lock, email)

def syncUsers(lock, email=None):
    # DB connection
    dbconnection = db.connect()

    # acquires lock
    with lock:
        logger.info("Worker users starting synchronization")
        try:
            if email:
                users = q(User).filter('email', email).get()
            else:
                users = q(User).get()
            """
            update local user table
            """
            if len(users)>0:
                local_users = db.users()
                # Add users from Registry unkown from local DB
                # this is used to bootstrap with init_user script
                for u in users:
                    #print("looking for {} in local db".format(u.id))
                    if not db.get(dbconnection, table='users', id=u.id):
                        #print("this user is not in local db, add it")
                        logger.info("Found new user from Registry: %s" % u.id)
                        db.users(dbconnection, u.dict(), u.id)
                # Update users known in local DB
                for lu in local_users:
                    logger.info("Synchronize user %s" % lu['id'])
                    try:
                        # add status if not present and update on db
                        if not 'status' in lu:
                            lu['status'] = Status.ENABLED
                            lu['enabled'] = format_date()
                        if not users.has(lu['id']) and lu['status'] is not Status.PENDING:
                            # delete user that has been deleted in Reg
                            db.delete(dbconnection, 'users', lu['id'])
                            logger.info("User {} deleted".format(lu['id']))
                        else:
                            remote_user = next((item for item in users if item.id == lu['id']), False)
                            if remote_user:
                                # merge fields of local user with remote
                                # keep local values for
                                # password, private_key, public_key and generate_keys
                                updated_user = remote_user.merge(dbconnection)
                                updated_user = updated_user.dict()
                                # if user has private key
                                # update its Credentials
                                if 'private_key' in updated_user and updated_user['private_key'] is not None:
                                    updated_user = update_credentials(updated_user)
                                # Update user
                                #logger.debug("Update user %s" % updated_user['id'])
                                db.users(dbconnection, updated_user, updated_user['id'])
                    except Exception as e:
                        logger.warning("Could not synchronize user %s" % lu['id'])
                        logger.exception(e)
                        continue

            else:
                logger.warning("Query users is empty, check myslicelib and the connection with SFA Registry")
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.exception(e)

        logger.info("Worker users finished period synchronization") 
