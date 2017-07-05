#
#   MySlice version 2
#
#   Activity process service: manages events and requests
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##

import signal
import threading
from queue import Queue

import myslice.db as db
import rethinkdb as r

from myslice.db import connect, changes, events
from myslice.db.activity import Event, EventStatus
from myslice.services.workers.events import run as manageEvents
import myslice.lib.log as logging

logger = logging.getLogger("activity")

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

    dbconnection = connect()

    ##
    # Watch for changes on the activity table and send the event/request
    # to the running threads (via Queue).
    # A global watch feed is needed to permit spawning more threads to manage
    # events and requests
    #feed = r.db('myslice').table('activity').changes().run(dbconnection)
    logger.debug("Starting to listen for the changes")
    feed = changes(dbconnection, table='activity', status="NEW")

    ##
    # Process events that were not watched 
    # while Server process was not running
    # myslice/bin/myslice-server
    new_events = events(dbconnection, status="NEW")
    for ev in new_events:
        try:
            event = Event(ev)
            if event.status != event.previous_status:
                logger.debug("Add event %s to Events queue" % (event.id))
                qEvents.put(event)
        except Exception as e:
            logger.exception(e)
            if 'id' in ev:
                logger.error("Problem with event: {}".format(ev['id']))

    for activity in feed:
        logger.debug("Change in activity feed")
        try:
            if activity['new_val']['status'] == "NEW":
                logger.debug("NEW event in activity feed")
                event = Event(activity['new_val'])
                # If the status of the event changes then process it
                if event.status != event.previous_status:
                    logger.debug("Add event %s to Events queue" % (event.id))
                    qEvents.put(event)
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.exception(e)
            if 'new_val' in activity and 'id' in activity['new_val']:
                logger.error("Problem with event: {}".format(activity['new_val']['id']))

    logger.critical("Service activity stopped")
    # waits for the thread to finish
    for x in threads:
        x.join()
