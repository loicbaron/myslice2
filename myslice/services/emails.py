#
#   MySlice version 2
#
#   Activity process service: manages emails
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##

import logging
import signal
import threading
from queue import Queue
from myslice.db import connect, changes
from myslice.db.activity import Event
from myslice.services.workers.emails import request_run as manageRequests
from myslice.services.workers.emails import approve_run as manageApproved
from myslice.services.workers.emails import deny_run as manageDenied

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

    qRequests = Queue()
    qDenied = Queue()
    qApproved = Queue()
    sApproving = set()

    threads = []
    for y in range(1):
        t = threading.Thread(target=manageRequests, args=(qRequests,))
        t.daemon = True
        threads.append(t)
        t.start()
    
    for y in range(1):
        t = threading.Thread(target=manageApproved, args=(qApproved,))
        t.daemon = True
        threads.append(t)
        t.start()
    
    for y in range(1):
        t = threading.Thread(target=manageDenied, args=(qDenied,))
        t.daemon = True
        threads.append(t)
        t.start()

    feed = changes(table='activity')
    for activity in feed:
        try:
            event = Event(activity['new_val'])
        except Exception as e:
            logger.error("Problem with event: {}".format(e))
        else:
            print(event)
            if event.isPending():
                qRequests.put(event)
            if event.isDenied():
                logger.info("event {} is denied".format(event.id))
                qDenied.put(event)
            if event.isApproved():
                sApproving.add(event.id)
            if event.id in sApproving:
                if event.isSuccess():
                    qApproved.put(event)
                else:
                    logger.error("Somethong Wrong with the approved event during the process".format(event.id))

    # waits for the thread to finish
    for x in threads:
        x.join()
