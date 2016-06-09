#
#   MySlice version 2
#
#   User service: manages user scope events 
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##
import pprint
import logging
import signal
import threading
from queue import Queue
from myslice.db.activity import Event, ObjectType
from myslice.db import connect, changes, events
from myslice.services.workers.users import events_run as manageUsersEvents
from myslice.services.workers.users import sync as syncUsers

logger = logging.getLogger('myslice.service.activity')

def receive_signal(signum, stack):
    logger.info('Received signal %s', signum)

    raise SystemExit('Exiting')

def run():
    """

    """
    signal.signal(signal.SIGINT, receive_signal)
    signal.signal(signal.SIGTERM, receive_signal)
    signal.signal(signal.SIGHUP, receive_signal)

    logger.info("Service users starting")

    # db connection is shared between threads
    qUserEvents = Queue()
    lock = threading.Lock()

    threads = []
    for y in range(1):
        t = threading.Thread(target=manageUsersEvents, args=(lock, qUserEvents))
        t.daemon = True
        threads.append(t)
        t.start()

    for y in range(1):
        t = threading.Thread(target=syncUsers, args=(lock, ))
        t.daemon = True
        threads.append(t)
        t.start()

    dbconnection = connect()

    ##
    # Watch for changes on the activity table
    feed = changes(dbconnection, table='activity', status=["WAITING", "APPROVED"])
    ##
    # Process events that were not watched 
    # while Server process was not running
    # myslice/bin/myslice-server
    new_events = events(dbconnection, status=["WAITING", "APPROVED"])
    for ev in new_events:
        try:
            event = Event(ev)
        except Exception as e:
            logger.error("Problem with event: {}".format(e))
        else:
            if event.object.type == ObjectType.USER:
                qUserEvents.put(event)

    for activity in feed:
        try:
            event = Event(activity['new_val'])
        except Exception as e:
            logger.error("Problem with event: {}".format(e)) 
        else:
            if event.object.type == ObjectType.USER:
                # event.isReady() = Request APPROVED or Event WAITING
                qUserEvents.put(event)

                
    for x in threads:
        x.join()

