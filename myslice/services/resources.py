##
#   MySlice version 2
#
#   Experiments process service: will keep the list of slices and projects configured in sync
#   Will also manage slice/project creation, deletetion, status etc.
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##
import pprint
import logging
import signal
import threading
from queue import Queue
from myslice.db.activity import Event, ObjectType
from myslice.db import changes
from myslice.services.workers.resources import sync as syncResources
from myslice.services.workers.leases import sync as syncLeases

logger = logging.getLogger('myslice.service.resources')

def receive_signal(signum, stack):
    logger.info('Received signal %s', signum)

    raise SystemExit('Exiting')

def run():
    """
    A Process that will manage Projects and Slices 
    """
    signal.signal(signal.SIGINT, receive_signal)
    signal.signal(signal.SIGTERM, receive_signal)
    signal.signal(signal.SIGHUP, receive_signal)

    logger.info("Service resources starting")

    # db connection is shared between threads
    lock = threading.Lock()

    # threads
    threads = []

    # resources sync
    for y in range(1):
        t = threading.Thread(target=syncResources, args=(lock,))
        t.daemon = True
        threads.append(t)
        t.start()

    # resources sync
    for y in range(1):
        t = threading.Thread(target=syncLeases, args=(lock,))
        t.daemon = True
        threads.append(t)
        t.start()

    # waits for the thread to finish
    for x in threads:
        x.join()
