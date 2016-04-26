##
#   MySlice version 2
#
#   Authoritiess thread workers
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>, Loïc Baron <loic.baron@lip6.fr>
##

import logging
import time
import myslice.db as db
from myslice.lib import Status
from myslice.lib.util import format_date

from myslice.db.activity import Event, EventAction, EventStatus, Object, ObjectType 
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

                    # TODO: CREATE & DELETE
                    # if event.creatingObject():
                    # if event.deletingObject():

                    if event.updatingObject():
                        result = event.data

                    if event.addingObject():

                        authority = Authority(db.get(dbconnection, table='authorities', id=event.object.id))
                        
                        if event.data['type'] == 'USER':
                            user.addKey(event.data['key'])
                            result = user.save()

                    if event.removingObject():

                        user = User(db.get(dbconnection, table='authorities', id=event.object.id))
                        
                        if event.data['type'] == 'USER':
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
                    print(db.get(dbconnection, table='authorities', id=event.object.id))
                    event.setSuccess()
                
                db.dispatch(dbconnection, event)


def pendings_run(lock, qAuthorityPendings):
    """
    Process the user request directly
    """
    event = Event(qAuthorityPendings.get())
    
    dbconnection = connect()
    user = User(db.get(dbconnection, table='users', id=event.user))
    authority = Authority(db.get(dbconnection, table='authorities', id=event.object.id))
    if authority:
        upper_authority = Authority(db.get(dbconnection, table='authorities', id=authority.authority))
    else:
        upper_authority = Authority(db.get(dbconnection, table='authorities', id=event.object.id))

    if event.user in authority.pi_users or event.user in upper_authority.pi_users:
        event.setApproved()

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
