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
from myslice.db.activity import Event, EventStatus
from myslice.db import changes
from myslice.services.workers.projects import sync as syncProjects
from myslice.services.workers.slices import sync as syncSlices

logger = logging.getLogger('myslice.service.experiments')

def run():
    """
    A thread that will check resource availability and information
    """
    logger.info("Service experiments starting")


    lock = threading.Lock()

    # threads
    threads = []

    # projects sync
    t = threading.Thread(target=syncProjects, args=(lock,))
    t.daemon = True
    threads.append(t)
    t.start()

    # slices sync
    t = threading.Thread(target=syncSlices, args=(lock,))
    t.daemon = True
    threads.append(t)
    t.start()

    ##
    ## TOTO: watch for changes to slices and projects
    feed = changes(table='events')
    for change in feed:
        with lock:
            print(change)
            ev = Event(change['new_val'])

            pprint.pprint(ev)

            #ev.status = EventStatus.APPROVED

            #ev.dispatch()



    # update slice table
    #lslices = db.slices(dbconnection, slices.dict())

    # while True:
    #
    #
    #     result = r.setup(resource)
    #     print result
    #     if not result['status'] :
    #         logger.info("%s : Failed SSH access (%s)" % (resource, result['message']))
    #     else :
    #         logger.info("%s : Setup complete" % (resource))
    #
    #     s.resource(c, {
    #         "hostname": node.hostname,
    #         "state": node.boot_state,
    #         "access" : result
    #     })

        # ''' send OML stream '''
        # oml.availability(node.hostname, availability)