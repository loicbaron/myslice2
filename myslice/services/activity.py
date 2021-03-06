#
#   MySlice version 2
#
#   Activity process service: manages events and requests
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##
from multiprocessing import Process
import signal
import threading
from queue import Queue

import random

import myslice.db as db
import rethinkdb as r

from myslice.db import connect, changes, events
from myslice.db.activity import Event, EventStatus
from myslice.services.workers.events import run as manageEvents
import myslice.lib.log as logging

import zmq
import pickle
import json


logger = logging.getLogger()


def receive_signal(signum, stack):
    logger.info('Received signal %s', signum)
    raise SystemExit('Exiting')

def run():
    """

    """
    signal.signal(signal.SIGINT, receive_signal)
    signal.signal(signal.SIGTERM, receive_signal)
    signal.signal(signal.SIGHUP, receive_signal)

    qEvents = Queue()

    threads = []
    for y in range(1):
        t = threading.Thread(target=manageEvents, args=(qEvents,))
        t.daemon = True
        threads.append(t)
        t.start()

    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt_string(zmq.SUBSCRIBE, 'activity')
    socket.connect("tcp://localhost:6002")
    logger.info("[activity] Collecting updates from ZMQ bus for activity")

    while True:
        logger.debug("[activity]Change in activity feed")

        topic, zmqmessage = socket.recv_multipart()
        activity = pickle.loads(zmqmessage)


        logger.debug("[activity]{0}: {1}".format(topic, activity))

        try:
            event = Event(activity['new_val'])
            logger.debug("[activity] Adding event %s to Events queue" % (event.id))
            qEvents.put(event)

            #for debbuging purposes

        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.exception(e)
            if 'new_val' in activity and 'id' in activity['new_val']:
                logger.error("[activity] Problem with event: {}".format(activity['new_val']['id']))
            continue

    logger.critical("Service activity stopped")
    # waits for the thread to finish
    for x in threads:
        x.join()

if __name__ == '__main__':
    Process(target=run,).start()