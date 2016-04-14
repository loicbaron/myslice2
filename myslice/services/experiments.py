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
import threading
from queue import Queue
from myslice.db.activity import Event, ObjectType
from myslice.db import changes
from myslice.services.workers.projects import sync as syncProjects, manageProjects
from myslice.services.workers.slices import sync as syncSlices

logger = logging.getLogger('myslice.service.experiments')

def run():
    """
    A thread that will check resource availability and information
    """
    logger.info("Service experiments starting")


    lock = threading.Lock()

    qProjects = Queue()
    qSlices = Queue()

    # threads
    threads = []

    # projects sync
    # t = threading.Thread(target=syncProjects, args=(lock,))
    # t.daemon = True
    # threads.append(t)
    # t.start()

    # projects manager
    t = threading.Thread(target=manageProjects, args=(lock, qProjects))
    t.daemon = True
    threads.append(t)
    t.start()

    # slices sync
    # t = threading.Thread(target=syncSlices, args=(lock,))
    # t.daemon = True
    # threads.append(t)
    # t.start()

    # slices manager
    # t = threading.Thread(target=manageSlices, args=(lock, qSlices))
    # t.daemon = True
    # threads.append(t)
    # t.start()

    ##
    # will watch for incoming events/requests and pass them to
    # the appropriate thread group
    feed = changes(table='activity')
    for activity in feed:
        try:
            event = Event(activity['new_val'])
        except Exception as e:
            logger.error("Problem with event: {}".format(e))
        else:
            if event.isReady():
                if event.object.type == ObjectType.PROJECT:
                    qProjects.put(event)
                if event.object.type == ObjectType.SLICE:
                    qSlices.put(event)

    # waits for the thread to finish
    for x in threads:
        x.join()