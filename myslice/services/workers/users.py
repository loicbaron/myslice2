##
#   MySlice version 2
#
#   Users thread workers
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##
import time
import myslice.db as db
from myslice.lib import Status

from myslice.lib.authentication import UserSetup
from myslice import myslicelibsetup

from myslice.lib.util import format_date
import myslice.lib.log as logging

from myslice.db.activity import Event
from myslice.db import connect
from myslice.db.user import User
from myslicelib.query import q


logger = logging.getLogger("users")


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
            db.dispatch(dbconnection, event)
            continue
        else:
            logger.info("Processing event from user {}".format(event.user))
            with lock:
                try:
                    event.setRunning()
                    event.logInfo("Event is running")
                    logger.debug("Event %s is running" % event.id)
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
                        user = User(db.get(dbconnection, table='users', id=event.object.id))
                        if not user:
                            raise Exception("User doesn't exist")
                        user.id = event.object.id
                        isSuccess = user.delete(dbconnection, user_setup)
                    ##
                    # Updating user
                    if event.updatingObject():
                        logger.info("Updating user {}".format(event.object.id))
                        user = User(event.data)
                        local_user = User(db.get(dbconnection, table='users', id=event.object.id))
                        # we don't allow users to change their email
                        user.email = local_user.email
                        user.id = event.object.id
                        isSuccess = user.save(dbconnection, user_setup)
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    logger.error("Problem updating user: {} - {}".format(event.object.id, e))
                    event.logError(str(e))
                    event.setError()
                    continue

                if isSuccess:
                    event.setSuccess()
                    event.logInfo("Event success")
                    logger.debug("Event %s Success" % event.id)
                else:
                    logger.error("Error event {}: action failed".format(event.id))
                    event.setError()
                    event.logError("Error in worker users: action failed")
            ##
            # we then dispatch the event
            db.dispatch(dbconnection, event)

def update_credentials(dbconnection, user):
    # We can only get credentials for users that have a private key stored in db
    if 'private_key' in user and user['private_key'] is not None:
        try:
            u = User(user)
            user_setup = UserSetup(u, myslicelibsetup.endpoints)
            if u.hrn == "onelab.myslice":
                c = u.getCredentials(setup=user_setup)
            else:
                c = u.getCredentials(setup=user_setup, delegate_to="onelab.myslice")
            u.private_key = user['private_key']
            u.keys = [u.public_key]
            return u.dict()
        except Exception as e:
            logger.warning("Key missmatch between local and Registry")
            logger.warning("Trying to update the Registry")
            u.save(dbconnection)
    return user

def sync(lock, email=None, job=True):
    """
    A thread that will sync users with the local rethinkdb
    """

    if job:
        while True:
            try:
                syncUsers(lock, email)
            except Exception as e:
                logger.exception(e)
                continue

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
                # Add users from Registry unkown from local DB
                # this is used to bootstrap with init_user script
                for u in users:
                    logger.debug("looking for {} in local db".format(u.id))
                    if not db.get(dbconnection, table='users', id=u.id):
                        local_users = db.get(dbconnection, table='users')
                        logger.warning("Number of users in local db: %s" % len(local_users))
                        #print("this user is not in local db, add it")
                        logger.info("Found new user from Registry: %s" % u.id)
                        #logger.info("We don't add the missing users yet, as portal is the single point of entry")
                        db.users(dbconnection, u.dict())

                local_users = db.get(dbconnection, table='users')
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
                                    updated_user = update_credentials(dbconnection, updated_user)
                                # Update user
                                #logger.debug("Update user %s" % updated_user['id'])
                                db.users(dbconnection, updated_user, updated_user['id'])
                    except Exception as e:
                        logger.warning("Could not synchronize user %s" % lu['id'])
                        logger.exception(e)
                        raise

            else:
                logger.warning("Query users is empty, check myslicelib and the connection with SFA Registry")
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.exception(e)
            raise 

        logger.info("Worker users finished period synchronization") 
