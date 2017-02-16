##
#   MySlice version 2
#
#   Experiments process service: will keep the list of slices and projects configured in sync
#   Will also manage slice/project creation, deletetion, status etc.
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
#            Loïc Baron <loic.baron@lip6.fr>
##

import logging
import signal
import threading
from queue import Queue
import myslice.db as db
from myslice.db import changes, connect, events
from myslice.db.activity import Event, ObjectType
from myslice.services.workers.leases import events_run as manageLeases, sync as syncLeases

logger = logging.getLogger('myslice.service.leases')

def receive_signal(signum, stack):
    logger.info('Received signal %s', signum)

    raise SystemExit('Exiting')

def run():
    """
    A Process that will manage Leases 
    """
    signal.signal(signal.SIGINT, receive_signal)
    signal.signal(signal.SIGTERM, receive_signal)
    signal.signal(signal.SIGHUP, receive_signal)

    logger.info("Service leases starting")

    # db connection is shared between threads
    qLeases = Queue()
    lock = threading.Lock()

    # threads
    threads = []

    # leases manager
    for y in range(1):
        t = threading.Thread(target=manageLeases, args=(lock, qLeases))
        t.daemon = True
        threads.append(t)
        t.start()

    # leases sync
    for y in range(1):
        t = threading.Thread(target=syncLeases, args=(lock,))
        t.daemon = True
        threads.append(t)
        t.start()

    dbconnection = connect()

    ##
    # will watch for incoming events/requests and pass them to
    # the appropriate thread group
    feed = changes(dbconnection, table='activity', status=['WAITING', 'APPROVED'])
    ##
    # Process events that were not watched 
    # while Server process was not running
    # myslice/bin/myslice-server
    wa_events = events(dbconnection, status=['WAITING', 'APPROVED'])
    for ev in wa_events:
        try:
            event = Event(ev)
        except Exception as e:
            logger.error("Problem with event: {}".format(e))
        else:
            if event.object.type == ObjectType.LEASE:
                qLeases.put(event)

    for activity in feed:
        try:
            event = Event(activity['new_val'])
        except Exception as e:
            logger.error("Problem with event: {}".format(e))
        else:
            if event.object.type == ObjectType.LEASE:
                qLeases.put(event)

    # waits for the thread to finish
    for x in threads:
        x.join()
