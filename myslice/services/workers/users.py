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


def events_run(qUserEvents):
    """
    Process the user request directly
    """

    logger.info("Worker users events starting") 

    # feed = changes(c=c, table='events')
    # for ev in feed:
        
    #     event = Event(ev['new_val'])

    # db connection is shared between threads
    dbconnection = connect()

    while True:

        try:
            event = Event(qUserEvents.get())
        except Exception as e:
            logger.error("Problem with event: {}".format(e))
        finally:
            logger.info("Processing event from user {}".format(event.user))
                
            result = None

            try:
                if event.action == EventAction.MOD:
                    
                    result = event.data

                if event.action == EventAction.ADD:

                    user = User(db.get(dbconnection, table='users', id=event.user))
                    
                    if event.data['type'] == 'KEY':
                        user.keys = ['!@#$%^']
                        user.addKey(event.data['key'])

                        result = user.save()

                if event.action == EventAction.DEL:

                    user = User(db.get(dbconnection, table='users', id=event.user))
                    
                    if event.data['type'] == 'KEY':
                        user.delKey(event.data['key'])
                        result = user.save()


            except Exception as e:
                logger.error("Problem with event: {}".format(e))
                event.status = EventStatus.ERROR
                 
            if result:
                print(result)
                db.users(dbconnection, result)
                event.status = EventStatus.SUCCESS
            
            db.dispatch(dbconnection, event)


def requests_run(q):
    """
    Process the user request directly
    """
    pass
    # logger.info("Worker users requests starting") 

    # feed = changes(c=c, table='requests')
    # for request in feed:
    #     print(request)
    #     try:
    #         req = Request(request['new_val'])
    #     except Exception as e:
    #         logger.error("Problem with request: {}".format(e))
    #     finally:
    #         logger.info("Processing request from user {}".format(req.user))

    #         # get the user
    #         user = q(User).id(req.user).get()

    #         # retrieve the event
    #         ev = Event(event(req.event))

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

            """
            update local slice table
            """
            lusers = db.users(dbconnection, users.dict())

            for ls in lusers :
                if not users.has(ls['id']) and ls['status'] is not Status.PENDING:
                    # delete resourc that have been deleted elsewhere
                    db.delete(dbconnection, 'users', ls['id'])
                    logger.info("User {} deleted".format(ls['id']))

                # add status if not present and update on db
                if not 'status' in ls:
                    ls['status'] = Status.ENABLED
                    ls['enabled'] = format_date()
                    db.users(dbconnection, ls)

        # sleep
        time.sleep(86400)