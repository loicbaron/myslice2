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
from myslice.db import connect
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

    threads = []
    for y in range(1):
        t = threading.Thread(target=manageEvents)
        t.daemon = True
        threads.append(t)
        t.start()

    for y in range(1):
        t = threading.Thread(target=manageRequests)
        t.daemon = True
        threads.append(t)
        t.start()

    for x in threads:
        x.join()