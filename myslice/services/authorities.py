#
#   MySlice version 2
#
#   Authorities service: manages authority scope events 
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>, Loïc Baron <loic.baron@lip6.fr>
##
import pprint
import logging
import signal
import threading
from queue import Queue
from myslice.db.activity import Event, ObjectType
from myslice.db import connect, changes, events
from myslice.services.workers.authorities import events_run as manageAuthoritiesEvents
from myslice.services.workers.authorities import sync as syncAuthorities

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

    logger.info("Service authorities starting")

    # db connection is shared between threads
    qAuthorityEvents = Queue()
    lock = threading.Lock()

    threads = []
    for y in range(1):
        t = threading.Thread(target=manageAuthoritiesEvents, args=(lock, qAuthorityEvents))
        t.daemon = True
        threads.append(t)
        t.start()

    for y in range(1):
        t = threading.Thread(target=syncAuthorities, args=(lock, ))
        t.daemon = True
        threads.append(t)
        t.start()

    dbconnection = connect()

    ##
    # will watch for incoming events/requests and pass them to
    # the appropriate thread group
    feed = changes(dbconnection, table='activity', status=["WAITING", "APPROVED"])
    for activity in feed:
        try:
            event = Event(activity['new_val'])
        except Exception as e:
            logger.error("Problem with event: {}".format(e)) 
        else:
            if event.object.type == ObjectType.AUTHORITY:
                # event.isReady() = Request APPROVED or Event WAITING
                qAuthorityEvents.put(event)

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
            if event.object.type == ObjectType.AUTHORITY:
                qAuthorityEvents.put(event)

    for x in threads:
        x.join()

