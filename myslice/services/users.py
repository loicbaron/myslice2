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

from myslice import config
from myslice.db.activity import Event, ObjectType
from myslice.db import connect, changes, events
from myslice.services.workers.users import events_run as manageUsersEvents
from myslice.services.workers.password import events_run as managePasswordEvents
from myslice.services.workers.users import sync as syncUsers
import myslice.lib.log as logging
from myslice import config
import zmq
import pickle

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

    # dbconnection = connect()
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

    if config.services['users']['sync']:
        for y in range(1):
            t = threading.Thread(target=syncUsers, args=(lock, ))
            t.daemon = True
            threads.append(t)
            t.start()

    ##
    # Watch for changes on the activity table
    # feed = r.db('myslice').table('activity').changes().run(dbconnection)
        # .filter(lambda change: change['new_val']['status'] == status) \
        # .filter(lambda change: change['new_val']['status'] == status) \

    #feed = changes(dbconnection, table='activity', status=["WAITING", "APPROVED"])

    ##
    # Process events that were not watched 
    # while Server process was not running
    # myslice/bin/myslice-server
    # new_events = events(dbconnection, status=["WAITING", "APPROVED"])
    # for ev in new_events:
    #     try:
    #         event = Event(ev)
    #     except Exception as e:
    #         logger.exception(e)
    #         logger.error("Problem with event: {}".format(e))
    #     else:
    #         if event.object.type == ObjectType.USER:
    #             logger.debug("Add event %s to %s queue" % (event.id, event.object.type))
    #             qUserEvents.put(event)
    #
    #         if event.object.type == ObjectType.PASSWORD:
    #             logger.debug("Add event %s to %s queue" % (event.id, event.object.type))
    #             qPasswordEvents.put(event)

    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt_string(zmq.SUBSCRIBE, 'users')
    socket.connect("tcp://localhost:6002")
    logger.info("[emails] Collecting updates from ZMQ bus for activity")

    should_continue = True
    while should_continue:
        logger.debug("[users] Change in emails feed")

        topic, zmqmessage = socket.recv_multipart()
        activity = pickle.loads(zmqmessage)

        logger.debug("[users] {0}: {1}".format(topic, activity))
        try:
            event = Event(activity['new_val'])

            if event.isReady():

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

