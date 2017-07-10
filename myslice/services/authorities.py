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
from myslice import config

import zmq
import pickle

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

    if config.services['authorities']['sync']:
        for y in range(1):
            t = threading.Thread(target=syncAuthorities, args=(lock, ))
            t.daemon = True
            threads.append(t)
            t.start()

    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt_string(zmq.SUBSCRIBE, 'authorities')
    socket.connect("tcp://localhost:6002")
    logger.info("[authorities] Collecting updates from ZMQ bus for activity")

    should_continue = True
    while should_continue:
        logger.debug("[authorities]Change in authorities feed")

        topic, zmqmessage = socket.recv_multipart()
        activity = pickle.loads(zmqmessage)

        logger.debug("[authorities]{0}: {1}".format(topic, activity))

        try:
            event = Event(activity['new_val'])
            logger.debug("[authorities] Add event %s to %s queue" % (event.id, event.object.type))
            qAuthorityEvents.put(event)


        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.exception(e)
            if 'new_val' in activity and 'id' in activity['new_val']:
                logger.error("[authorities] Problem with event: {}".format(activity['new_val']['id']))
            else:
                logger.error("[authorities] Event is malformed: {}".format(activity))


    logger.critical("[authorities] Service authorities stopped")
    for x in threads:
        x.join()

