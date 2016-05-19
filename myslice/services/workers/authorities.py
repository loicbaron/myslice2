##
#   MySlice version 2
#
#   Authoritiess thread workers
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>, Loïc Baron <loic.baron@lip6.fr>
##

import json
import logging
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

logger = logging.getLogger('myslice.service.authorities')


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
            logger.error("Problem with event: {}".format(e))
        else:
            logger.info("Processing event from user {}".format(event.user))
            
            with lock:
                try:
                    event.setRunning()
                    isSuccess = False
                    
                    if event.creatingObject():

                        auth = Authority(event.data)
                        auth.id = event.object.id
                        isOK1 = auth.save(dbconnection)

                        pi = User(event.data['pi'])
                        auth_head = '+'.join(event.object.id.split('+')[:-2])
                        pi.id = auth_head + "+user+{}".format(event.data['pi']['shortname'])
                        isOK2 = pi.save(dbconnection)

                        auth.addPi(pi)
                        isOK3 = auth.save(dbconnection)
                        isSuccess = isOK1 & isOK2 & isOK3

                        #    # if user is admin, add him as PI of the Authority
                        #    # XXX Do we want that?
                        #    pi_local_dict = db.get(dbconnection, table='users', id=event.user)
                        #    u = User(pi_local_dict)


                    if event.updatingObject():
                        logger.info("updating the object authority {}".format(event.object.id)) 
                        
                        auth = Authority(event.data)
                        auth.id = event.object.id
                        isSuccess = auth.save(dbconnection)

                    if event.deletingObject():
                        logger.info("deleting the object authority {}".format(event.object.id)) 
                        
                        auth = Authority(db.get(dbconnection, table='authorities', id=event.object.id))
                        if not auth:
                            raise Exception("Authority doesn't exist")
                        isSuccess = auth.delete(dbconnection)

                    if event.addingObject():
                        logger.info("adding data to the object authority {}".format(event.object.id)) 
                        
                        if event.data.type == DataType.USER:
                            raise Exception("Please use CREATE USER instead")
                        if event.data.type == DataType.PI:
                            auth = Authority(db.get(dbconnection, table='authorities', id=event.object.id))
                            for val in event.data.values:
                                pi = User(db.get(dbconnection, table='users', id=val))
                                auth.addPi(pi)
                            isSuccess = auth.save(dbconnection)

                    if event.removingObject():
                        logger.info("removing data from the object authority {}".format(event.object.id)) 

                        if event.data.type == DataType.USER:
                            raise Exception("Please use DELETE USER instead")
                        if event.data.type == DataType.PI:
                            auth = Authority(db.get(dbconnection, table='authorities', id=event.object.id))
                            for val in event.data.values:
                                pi = User(db.get(dbconnection, table='users', id=val))
                                auth.removePi(pi)
                            isSuccess = auth.save(dbconnection)

                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    logger.error("Problem with event: {}".format(e))
                    event.logError(str(e)) 
                
                if isSuccess:
                    event.setSuccess()
                else:
                    event.setError()
                
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

            authorities = q(Authority).get()

            """
            update local slice table
            """
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

 

            logger.info("Worker authorities finished period synchronization") 
        
        # sleep
        time.sleep(86400)
