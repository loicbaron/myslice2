##
#   MySlice version 2
#
#   Authoritiess thread workers
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>, Loïc Baron <loic.baron@lip6.fr>
##

import json
import time
from pprint import pprint
import myslice.db as db
from myslice.lib import Status
from myslice.lib.util import format_date

from myslice.db.activity import Event, ObjectType, DataType
from myslice.db import changes, connect
from myslice.db.user import User
from myslice.db.authority import Authority
from myslicelib.query import q
import myslice.lib.log as logging

logger = logging.getLogger("authorities")


def events_run(lock, qAuthorityEvents):
    """
    Process the authority after approval 
    """

    logger.info("Worker authorities events starting") 

    # db connection is shared between threads
    dbconnection = connect()

    while True:
        try:
            event = Event(qAuthorityEvents.get())
        except Exception as e:
            logger.exception("Problem with event: {}".format(e))
            continue
        else:
            logger.info("Processing event {} from user {}".format(event.id, event.user))
            
            with lock:
                try:
                    event.setRunning()
                    event.logInfo("Event is running")
                    logger.debug("Event %s is running" % event.id)
                    isSuccess = False
                    
                    if event.creatingObject() or event.updatingObject():
                        try:
                            logger.info("creating or updating the object authority {}".format(event.object.id))
                            auth = Authority(event.data)
                        except Exception as e:
                            logger.error("There has been an error while creating authority")
                            logger.error(e, exc_info=True)
                            raise
                        else:
                            auth.id = event.object.id
                            isSuccess = auth.save(dbconnection)
                    else:
                        a = db.get(dbconnection, table='authorities', id=event.object.id)
                        if not a:
                            raise Exception("Authority doesn't exist")
                        auth = Authority(a)

                    if event.deletingObject():
                        logger.info("deleting the object authority {}".format(event.object.id)) 
                        isSuccess = auth.delete(dbconnection)

                    if event.addingObject():
                        logger.info("adding data to the object authority {}".format(event.object.id)) 
                        
                        if event.data.type == DataType.USER:
                            raise Exception("Please use CREATE USER instead")
                        if event.data.type == DataType.PI:
                            for val in event.data.values:
                                pi = User(db.get(dbconnection, table='users', id=val))
                                auth.addPi(pi)
                            isSuccess = auth.save(dbconnection)

                    if event.removingObject():
                        logger.info("removing data from the object authority {}".format(event.object.id)) 

                        if event.data.type == DataType.USER:
                            raise Exception("Please use DELETE USER instead")
                        if event.data.type == DataType.PI:
                            for val in event.data.values:
                                pi = User(db.get(dbconnection, table='users', id=val))
                                auth.removePi(pi)
                            isSuccess = auth.save(dbconnection)

                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    logger.exception("Problem with event {}: {}".format(event.id,e))
                    event.logError("Error in worker authorities: {}".format(e))
                    event.setError()
                    continue

                if isSuccess:
                    event.setSuccess()
                    event.logInfo("Event success")
                    logger.debug("Event %s Success" % event.id)
                else:
                    logger.error("Error event {}: action failed".format(event.id))
                    event.setError()
                    event.logError("Error in worker authorities: action failed")
                
                db.dispatch(dbconnection, event)

def sync(lock):
    """
    A thread that will sync users with the local rethinkdb
    """

    while True:
        try:
            syncAuthorities(lock)
        except Exception as e:
            continue
        # sleep
        time.sleep(86400)

def syncAuthorities(lock):

    # DB connection
    dbconnection = db.connect()

    # acquires lock
    with lock:
        logger.info("Worker authorities starting period synchronization")

        authorities = q(Authority).get()

        """
        update local slice table
        """
        if len(authorities)>0:
            lauthorities = db.authorities(dbconnection, authorities.dict())
            for ls in lauthorities :
                # add status if not present and update on db
                if not 'status' in ls:
                    ls['status'] = Status.ENABLED
                    ls['enabled'] = format_date()
                    db.authorities(dbconnection, ls)

                if not authorities.has(ls['id']) and ls['status'] is not Status.PENDING:
                    # delete resourc that have been deleted elsewhere
                    db.delete(dbconnection, 'authorities', ls['id'])
                    logger.info("Authority {} deleted".format(ls['id']))
        else:
            logger.warning("Query authorities is empty, check myslicelib and the connection with SFA Registry")

        logger.info("Worker authorities finished period synchronization") 
