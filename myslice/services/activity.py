#
#   MySlice version 2
#
#   Activity process service: manages events and requests
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##

import logging
import signal
import threading
from queue import Queue
import myslice.db as db
from myslice.db import connect, changes
from myslice.db.activity import Event
from myslice.services.workers.events import run as manageEvents

logger = logging.getLogger('myslice.service.activity')

def receive_signal(signum, stack):
    logger.info('Received signal %s', signum)
    raise SystemExit('Exiting')

def process_event(ev):
    try:
        event = Event(ev)
    except Exception as e:
        logger.error("Problem with event: {}".format(e))
    else:
        if event.isNew():
            qEvents.put(event)

def run():
    """

    """
    signal.signal(signal.SIGINT, receive_signal)
    signal.signal(signal.SIGTERM, receive_signal)
    signal.signal(signal.SIGHUP, receive_signal)

    logger.info("Service activity starting")

    qEvents = Queue()

    threads = []
    for y in range(1):
        t = threading.Thread(target=manageEvents, args=(qEvents,))
        t.daemon = True
        threads.append(t)
        t.start()

    dbconnection = connect()

    ##
    # Process events that were not watched 
    # while Server process was not running
    # myslice/bin/myslice-server
    db_events = db.get(dbconnection, table='activity', filter={'status':"NEW"})
    for e in db_events:
        process_event(e)

    ##
    # Watch for changes on the activity table and send the event/request
    # to the running threads (via Queue).
    # A global watch feed is needed to permit spawning more threads to manage
    # events and requests
    feed = changes(dbconnection, table='activity')
    for activity in feed:
        process_event(activity['new_val'])

    # waits for the thread to finish
    for x in threads:
        x.join()
