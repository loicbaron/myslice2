##
#   MySlice version 2
#
#   Experiments process service: will keep the list of slices and projects configured in sync
#   Will also manage slice/project creation, deletetion, status etc.
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##

import logging
import signal
import threading
from queue import Queue
import myslice.db as db
from myslice.db import connect, changes
from myslice.db.activity import Event, ObjectType
from myslice.services.workers.projects import events_run as manageProjects, sync as syncProjects
from myslice.services.workers.slices import events_run as manageSlices, sync as syncSlices

logger = logging.getLogger('myslice.service.experiments')

def receive_signal(signum, stack):
    logger.info('Received signal %s', signum)

    raise SystemExit('Exiting')

def process_event(ev):
    try:
        event = Event(ev)
    except Exception as e:
        logger.error("Problem with event: {}".format(e))
    else:
        if event.isReady():
            if event.object.type == ObjectType.PROJECT:
                qProjects.put(event)
            if event.object.type == ObjectType.SLICE:
                qSlices.put(event)

def run():
    """
    A Process that will manage Projects and Slices 
    """
    signal.signal(signal.SIGINT, receive_signal)
    signal.signal(signal.SIGTERM, receive_signal)
    signal.signal(signal.SIGHUP, receive_signal)

    logger.info("Service experiments starting")

    # db connection is shared between threads
    qProjects = Queue()
    qSlices = Queue()
    lock = threading.Lock()

    # threads
    threads = []

    # projects manager
    for y in range(1):
        t = threading.Thread(target=manageProjects, args=(lock, qProjects))
        t.daemon = True
        threads.append(t)
        t.start()

    # projects sync
    for y in range(1):
        t = threading.Thread(target=syncProjects, args=(lock,))
        t.daemon = True
        threads.append(t)
        t.start()

    # slices manager
    for y in range(1):
        t = threading.Thread(target=manageSlices, args=(lock, qSlices))
        t.daemon = True
        threads.append(t)
        t.start()

    # slices sync
    for y in range(1):
        t = threading.Thread(target=syncSlices, args=(lock,))
        t.daemon = True
        threads.append(t)
        t.start()

    dbconnection = connect()

    ##
    # Process events that were not watched 
    # while Server process was not running
    # myslice/bin/myslice-server
    db_events = db.get(dbconnection, table='activity', filter={'status':"APPROVED"})
    #db_events = db.get(dbconnection, table='activity', filter={'status':"WAITING"})
    for e in db_events:
        process_event(e)

    ##
    # will watch for incoming events/requests and pass them to
    # the appropriate thread group
    feed = changes(dbconnection, table='activity')
    for activity in feed:
        process_event(activity['new_val'])

    # waits for the thread to finish
    for x in threads:
        x.join()
