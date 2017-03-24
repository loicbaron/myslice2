#
#   MySlice version 2
#
#   Authorities service: manages authority scope events 
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>, Loïc Baron <loic.baron@lip6.fr>
##
import pprint
import signal
import threading
from queue import Queue
from myslice.db.activity import Event, ObjectType
import rethinkdb as r
from myslice.db import connect, changes, events
from myslice.services.workers.authorities import events_run as manageAuthoritiesEvents
from myslice.services.workers.authorities import sync as syncAuthorities
import myslice.lib.log as logging

logger = logging.getLogger("authorities")

def receive_signal(signum, stack):
    logger.info('Received signal %s', signum)

    raise SystemExit('Exiting')

def run():
    """

    """
    signal.signal(signal.SIGINT, receive_signal)
    signal.signal(signal.SIGTERM, receive_signal)
    signal.signal(signal.SIGHUP, receive_signal)

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
    feed = r.db('myslice').table('activity').changes().run(dbconnection)
    #feed = changes(dbconnection, table='activity', status=["WAITING", "APPROVED"])

    ##
    # Process events that were not watched 
    # while Server process was not running
    # myslice/bin/myslice-server
    new_events = events(dbconnection, status=["WAITING", "APPROVED"])
    for ev in new_events:
        try:
            event = Event(ev)
        except Exception as e:
            logger.exception(e)
            logger.error("Problem with event: {}".format(e))
        else:
            if event.object.type == ObjectType.AUTHORITY:
                logger.debug("Add event %s to %s queue" % (event.id, event.object.type))
                qAuthorityEvents.put(event)

    for activity in feed:
        try:
            if activity['new_val']['status'] in ["WAITING","APPROVED"]:
                event = Event(activity['new_val'])
                if event.object.type == ObjectType.AUTHORITY:
                    # event.isReady() = Request APPROVED or Event WAITING
                    logger.debug("Add event %s to %s queue" % (event.id, event.object.type))
                    qAuthorityEvents.put(event)
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.exception(e)
            if 'new_val' in activity and 'id' in activity['new_val']:
                logger.error("Problem with event: {}".format(activity['new_val']['id']))


    logger.critical("Service authorities stopped")
    for x in threads:
        x.join()

