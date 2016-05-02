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

from myslice.db.activity import Event, ObjectType
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

                    if event.creatingObject() or event.updatingObject():
                        a = Authority(event.data)
                        a.id = event.object.id 
                        result = a.save()

                    if event.deletingObject():
                        result = q(Authority).id(event.object.id).delete()

                    if event.addingObject():
                        if event.data['type'] == ObjectType.USER:
                            raise Exception("Please use CREATE USER instead")
                        if event.data['type'] == ObjectType.PI:
                            a = Authority(db.get(dbconnection, table='authorities', id=event.object.id))
                            for val in event.data['values']:
                                pi = User(db.get(dbconnection, table='users', id=val))
                                a.addPi(pi)
                            result = a.save()

                    if event.removingObject():
                        if event.data['type'] == ObjectType.USER:
                            raise Exception("Please use DELETE USER instead")
                        if event.data['type'] == ObjectType.PI:
                            a = Authority(db.get(dbconnection, table='authorities', id=event.object.id))
                            for val in event.data['values']:
                                pi = User(db.get(dbconnection, table='users', id=val))
                                a.removePi(pi)
                            result = a.save()

                except Exception as e:
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
                        db.authorities(dbconnection, result, event.object.id)
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
