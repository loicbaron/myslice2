##
#   MySlice version 2
#
#   Events thread worker
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##

import myslice.db as db
from myslice.db import connect, dispatch
from myslice.db.activity import Event, ObjectType 
from myslice.db.user import User
import myslice.lib.log as logging

logger = logging.getLogger("activity")

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
            import traceback
            traceback.print_exc()
            logger.error("Problem with event: {}".format(e))
            event.logError("Error in worker activity: {}".format(e))
            event.setError()
            dispatch(dbconnection, event)
        else:
            try:
                logger.debug("%s - Manage event" % event.id)
                # TODO: if event.creatingObject()
                # Check if the event.object.id already exists or not
                # if it exists -> add a numer to the id & hrn to make it unique

                if event.object.type == ObjectType.PASSWORD:
                    event.setPending()
                    event.logInfo("Event is pending, please check your email")
                    logger.debug("Event %s is pending" % event.id)
                # Register a new object for a new user
                # id should be generated into the web to avoid duplicates
                elif event.isNew() and event.object.type in [ObjectType.USER, ObjectType.AUTHORITY] and event.user is None and event.creatingObject():
                    # The user must confirm his/her email
                    print("Event Type: %s" % type(event))
                    event.setConfirm()
                    logger.debug("Event %s is confirm" % event.id)
                    event.logInfo("Event is expecting your confirmation, please check your email")
                else:
                    logger.debug("%s - get user %s" % (event.id,event.user))
                    db_user = db.get(dbconnection, table='users', id=event.user)
                    if db_user:
                        user = User(db_user)
                        logger.debug("%s - Does user %s has privilege?" % (event.id, event.user))
                        if user.has_privilege(event):
                            logger.debug("%s - setWaiting" % event.id)
                            event.logInfo("Event waiting to be processed")
                            event.setWaiting()
                        else:
                            logger.debug("%s - setPending" % event.id)
                            event.logInfo("your user has no rights on %s, event pending until approved" % event.user)
                            event.setPending()
                    else:
                        event.setError()
                        logger.error("User {} not found in event {}".format(event.user, event.id))
                        event.logError("User %s not found" % event.user)
                        # raising an Exception here, blocks the REST API
                        #raise Exception("User %s not found" % event.user)
            except Exception as e:
                logger.error("Error processing Event")
                logger.error(event)
                import traceback
                logger.error(traceback.print_exc())
                traceback.print_exc()
                event.setError()
                event.logError(str(e))
                logger.error("Unable to fetch the user {} from db".format(event.user))
                logger.exception(e)

            # dispatch the updated event
            dispatch(dbconnection, event)
