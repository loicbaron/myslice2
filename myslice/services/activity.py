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
from myslice.db import connect, changes
from myslice.services.workers.events import run as manageEvents
from myslice.services.workers.requests import run as manageRequests

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

    logger.info("Service activity starting")

    qEvents = Queue()
    qRequests = Queue()

    threads = []
    for y in range(1):
        t = threading.Thread(target=manageEvents, args=(qEvents,))
        t.daemon = True
        threads.append(t)
        t.start()

    for y in range(1):
        t = threading.Thread(target=manageRequests, args=(qRequests,))
        t.daemon = True
        threads.append(t)
        t.start()

    ##
    # Watch for changes on the activity table and send the event/request
    # to the corresponding threads (via Queue).
    # A global watch feed is needed to permit spawning more threads to manage
    # events and requests
    feed = changes(table='activity')
    for activity in feed:
        if activity['new_val']['type'] == 'EVENT':
            qEvents.put(activity['new_val'])
        elif activity['new_val']['type'] == 'REQUEST':
            qRequests.put(activity['new_val'])

    # waits for the thread to finish
    for x in threads:
        x.join()