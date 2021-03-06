##
#   MySlice version 2
#
#   Experiments process service: will keep the list of slices and projects configured in sync
#   Will also manage slice/project creation, deletetion, status etc.
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##

import signal
import threading
from queue import Queue
import myslice.db as db
import rethinkdb as r
from myslice.db import changes, connect, events
from myslice.db.activity import Event, ObjectType
from myslice.services.workers.projects import events_run as manageProjects, sync as syncProjects
from myslice.services.workers.slices import events_run as manageSlices, sync as syncSlices
import myslice.lib.log as logging
from myslice import config
import zmq
import pickle

logger = logging.getLogger("experiments")

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

    # db connection is shared between threads
    qProjects = Queue()
    qSlices = Queue()
    lockProjects = threading.Lock()

    # threads
    threads = []

    # projects manager
    for y in range(1):
        t = threading.Thread(target=manageProjects, args=(lockProjects, qProjects))
        t.daemon = True
        threads.append(t)
        t.start()

    # projects sync
    if config.services['experiments']['sync']:
        for y in range(1):
            t = threading.Thread(target=syncProjects, args=(lockProjects,))
            t.daemon = True
            threads.append(t)
            t.start()

    # slices manager
    for y in range(1):
        t = threading.Thread(target=manageSlices, args=(qSlices,))
        t.daemon = True
        threads.append(t)
        t.start()

    # slices sync
    if config.services['experiments']['sync']:
        for y in range(1):
            t = threading.Thread(target=syncSlices)
            t.daemon = True
            threads.append(t)
            t.start()

    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt_string(zmq.SUBSCRIBE, 'experiments')
    socket.connect("tcp://localhost:6002")
    logger.info("[emails] Collecting updates from ZMQ bus for activity")

    while True:
        logger.debug("[emails]Change in emails feed")

        topic, zmqmessage = socket.recv_multipart()
        activity = pickle.loads(zmqmessage)

        logger.debug("[emails]{0}: {1}".format(topic, activity))

        try:
            # if activity['new_val']['status'] in ["WAITING","APPROVED"]:
            event = Event(activity['new_val'])
            if event.object.type == ObjectType.PROJECT:
                logger.debug("Add event %s to %s queue" % (event.id, event.object.type))
                qProjects.put(event)
            if event.object.type == ObjectType.SLICE:
                logger.debug("Add event %s to %s queue" % (event.id, event.object.type))
                qSlices.put(event)
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.exception(e)
            if 'new_val' in activity and 'id' in activity['new_val']:
                logger.error("Problem with event: {}".format(activity['new_val']['id']))
            continue

    logger.critical("Service experiments stopped")
    # waits for the thread to finish
    for x in threads:
        x.join()
