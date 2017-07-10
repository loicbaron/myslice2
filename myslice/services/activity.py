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
    for y in range(10):
        t = threading.Thread(target=manageEvents, args=(qEvents,))
        t.daemon = True
        threads.append(t)
        t.start()

    # Rethinkdb conncection
    # dbconnection = connect()
    #
    # Process events that were not watched
    # while Server process was not running
    # myslice/bin/myslice-server
    # new_events = events(dbconnection, status="NEW")
    # for ev in new_events:
    #     try:
    #         event = Event(ev)
    #         if event.status != event.previous_status:
    #             logger.debug("Add event %s to Events queue" % (event.id))
    #             qEvents.put(event)
    #     except Exception as e:
    #         logger.exception(e)
    #         if 'id' in ev:
    #             logger.error("Problem with event: {}".format(ev['id']))

    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt_string(zmq.SUBSCRIBE, 'activity')
    socket.connect("tcp://localhost:6002")
    logger.info("[activity] Collecting updates from ZMQ bus for activity")

    should_continue = True
    while should_continue:
        logger.debug("[activity]Change in activity feed")

        topic, zmqmessage = socket.recv_multipart()
        activity = pickle.loads(zmqmessage)


        logger.debug("[activity]{0}: {1}".format(topic, activity))

        try:
            event = Event(activity['new_val'])
            # If the status of the event changes then process it
            if event.status != event.previous_status:
                logger.debug("[activity] Adding event %s to Events queue" % (event.id))
                qEvents.put(event)
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.exception(e)
            if 'new_val' in activity and 'id' in activity['new_val']:
                logger.error("[activity] Problem with event: {}".format(activity['new_val']['id']))

    logger.critical("Service activity stopped")
    # waits for the thread to finish
    for x in threads:
        x.join()

if __name__ == '__main__':
    Process(target=run,).start()