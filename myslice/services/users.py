#
#   MySlice version 2
#
#   User service: manages user scope events 
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##
import signal
import threading
from queue import Queue
import rethinkdb as r
from myslice.db.activity import Event, ObjectType
from myslice.db import connect, changes, events
from myslice.services.workers.users import events_run as manageUsersEvents
from myslice.services.workers.password import events_run as managePasswordEvents
from myslice.services.workers.users import sync as syncUsers
import myslice.lib.log as logging

logger = logging.getLogger("users")

def receive_signal(signum, stack):
    logger.info('Received signal %s', signum)

    raise SystemExit('Exiting')

def run():
    """

    """
    signal.signal(signal.SIGINT, receive_signal)
    signal.signal(signal.SIGTERM, receive_signal)
    signal.signal(signal.SIGHUP, receive_signal)

    dbconnection = connect()
    # db connection is shared between threads
    qUserEvents = Queue()
    qPasswordEvents = Queue()
    lock = threading.Lock()

    threads = []
    for y in range(1):
        t = threading.Thread(target=manageUsersEvents, args=(lock, qUserEvents))
        t.daemon = True
        threads.append(t)
        t.start()

    for y in range(1):
        t = threading.Thread(target=managePasswordEvents, args=(lock, qPasswordEvents))
        t.daemon = True
        threads.append(t)
        t.start()

    for y in range(1):
        t = threading.Thread(target=syncUsers, args=(lock, ))
        t.daemon = True
        threads.append(t)
        t.start()

    ##
    # Watch for changes on the activity table
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
            if event.object.type == ObjectType.USER:
                logger.debug("Add event %s to %s queue" % (event.id, event.object.type))
                qUserEvents.put(event)

            if event.object.type == ObjectType.PASSWORD:
                logger.debug("Add event %s to %s queue" % (event.id, event.object.type))
                qPasswordEvents.put(event)

    for activity in feed:
        try:
            if activity['new_val']['status'] in ["WAITING","APPROVED"]:
                event = Event(activity['new_val'])
                if event.object.type == ObjectType.USER:
                    logger.debug("Add event %s to %s queue" % (event.id, event.object.type))
                    qUserEvents.put(event)

                if event.object.type == ObjectType.PASSWORD:
                    logger.debug("Add event %s to %s queue" % (event.id, event.object.type))
                    qPasswordEvents.put(event)
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.exception(e)
            if 'new_val' in activity and 'id' in activity['new_val']:
                logger.error("Problem with event: {}".format(activity['new_val']['id']))

    logger.critical("Service users stopped")
    for x in threads:
        x.join()

