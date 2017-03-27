##
#   MySlice version 2
#
#   Experiments process service: will keep the list of slices and projects configured in sync
#   Will also manage slice/project creation, deletetion, status etc.
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
#            Loïc Baron <loic.baron@lip6.fr>
##

import signal
import threading
from queue import Queue
import myslice.db as db
import rethinkdb as r
from myslice.db import changes, connect, events
from myslice.db.activity import Event, ObjectType
from myslice.services.workers.leases import events_run as manageLeases, sync as syncLeases
import myslice.lib.log as logging
from myslice import config

logger = logging.getLogger("leases")

def receive_signal(signum, stack):
    logger.info('Received signal %s', signum)

    raise SystemExit('Exiting')

def run():
    """
    A Process that will manage Leases 
    """
    signal.signal(signal.SIGINT, receive_signal)
    signal.signal(signal.SIGTERM, receive_signal)
    signal.signal(signal.SIGHUP, receive_signal)

    # db connection is shared between threads
    qLeases = Queue()
    lock = threading.Lock()

    # threads
    threads = []

    # leases manager
    for y in range(1):
        t = threading.Thread(target=manageLeases, args=(lock, qLeases))
        t.daemon = True
        threads.append(t)
        t.start()

    # leases sync
    if config.services['leases']['sync']:
        for y in range(1):
            t = threading.Thread(target=syncLeases, args=(lock,))
            t.daemon = True
            threads.append(t)
            t.start()

    dbconnection = connect()

    ##
    # will watch for incoming events/requests and pass them to
    # the appropriate thread group
    feed = r.db('myslice').table('activity').changes().run(dbconnection)
    #feed = changes(dbconnection, table='activity', status=['WAITING', 'APPROVED'])

    ##
    # Process events that were not watched 
    # while Server process was not running
    # myslice/bin/myslice-server
    wa_events = events(dbconnection, status=['WAITING', 'APPROVED'])
    for ev in wa_events:
        try:
            event = Event(ev)
        except Exception as e:
            logger.exception(e)
            logger.error("Problem with event: {}".format(e))
        else:
            if event.object.type == ObjectType.LEASE:
                logger.debug("Add event %s to %s queue" % (event.id, event.object.type))
                qLeases.put(event)

    for activity in feed:
        try:
            if activity['new_val']['status'] in ["WAITING","APPROVED"]:
                event = Event(activity['new_val'])
                if event.object.type == ObjectType.LEASE:
                    logger.debug("Add event %s to %s queue" % (event.id, event.object.type))
                    qLeases.put(event)
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.exception(e)
            if 'new_val' in activity and 'id' in activity['new_val']:
                logger.error("Problem with event: {}".format(activity['new_val']['id']))


    logger.critical("Service leases stopped")
    # waits for the thread to finish
    for x in threads:
        x.join()
