##
#   MySlice version 2
#
#   Projects thread workers
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
#            Loïc Baron <loic.baron@lip6.fr>
##

import time

import myslice.db as db
from myslice.lib import Status
from myslice.lib.util import format_date

from myslice.lib.authentication import UserSetup
from myslice import myslicelibsetup
from myslice.services.workers.slices import syncSlices

from myslice.db.activity import Event, ObjectType
from myslice.db import changes, connect
from myslice.db.user import User
from myslicelib.model.lease import Lease
from myslicelib.model.resource import Resource
from myslice.db.slice import Slice, SliceException, SliceWarningException
from myslicelib.query import q
import myslice.lib.log as logging

logger = logging.getLogger("leases")

def events_run(lock, qLeasesEvents):
    """
    Process the leases events
    """

    logger.info("Worker leases events starting") 

    # db connection is shared between threads
    dbconnection = connect()

    while True:
        try:
            event = Event(qLeasesEvents.get())
        except Exception as e:
            logger.error("Problem with event: {}".format(e))
            event.logError("Error in worker leases: {}".format(e))
            event.setError()
            db.dispatch(dbconnection, event)
            continue
        else:
            logger.info("Processing event from user {}".format(event.user))
            try:
                event.setRunning()
                event.logInfo("Event is running")
                logger.debug("Event %s is running" % event.id)
                isSuccess = False

                u = User(db.get(dbconnection, table='users', id=event.user))
                user_setup = UserSetup(u, myslicelibsetup.endpoints)

                if event.creatingObject(): 
                    leases = []
                    if isinstance(event.data, list):
                        for l in event.data:
                            slice_id = l['slice_id']
                            leases.append(Lease(l))
                    else:
                        slice_id = event.data['slice_id']
                        leases.append(Lease(event.data))
                    sli = Slice(db.get(dbconnection, table='slices', id=slice_id))
                    if not sli:
                        raise Exception("Slice doesn't exist")
                    for lease in leases:
                        for val in lease.resources:
                            r = db.get(dbconnection, table='resources', id=val)
                            # Add resource only if it exists in DB
                            if r is not None:
                                r = Resource(r)
                                sli.addResource(r)
                            else:
                                r = Resource({'id':val})
                                lease.removeResource(r)

                        if len(lease.resources) > 0:
                            sli.addLease(lease)
                        else:
                            raise Exception("Invalid resources")
                    isSuccess = sli.save(dbconnection, user_setup)

                if event.deletingObject(): 
                    lease = Lease(db.get(dbconnection, table='leases', id=event.object.id))
                    if not lease:
                        raise Exception("Lease doesn't exist")

                    sli = Slice(db.get(dbconnection, table='slices', id=event.data['slice_id']))
                    if not sli:
                        raise Exception("Slice doesn't exist")

                    for val in event.data['resources']:
                        r = Resource(db.get(dbconnection, table='resources', id=val))
                        # Remove resource only if it exists in DB
                        if r:
                            sli.removeResource(r)
                        else:
                            r = Resource({'id':val})
                            lease.removeResource(r)
                    sli.removeLease(lease)

                    isSuccess = sli.save(dbconnection, user_setup)

            except SliceException as e:
                # CREATE, DELETE
                # If at least one of the AMs replies with success, it's ok
                # If all AMs have failed -> Error 
                for err in e.stack:
                    event.logError("Error in worker leases: {}".format(err))
                    logger.error("Error in worker leases: {}".format(err))
                # XXX TO BE REFINED
                event.setError()
                continue

            except SliceWarningException as e:
                for err in e.stack:
                    event.logWarning(str(err))
                    logger.warning(str(err))
                event.setWarning()
                continue

            except Exception as e:
                import traceback
                traceback.print_exc()
                logger.error("Problem with event {}: {}".format(event.id,e))
                event.logError("Error in worker leases: {}".format(e))
                event.setError()
                continue
            else:
                if isSuccess:
                    event.setSuccess()
                    event.logInfo("Event success")
                    logger.debug("Event %s Success" % event.id)
                else:
                    logger.error("Error event {}: action failed".format(event.id))
                    event.setError()
                    event.logError("Error in worker leases: action failed")

            db.dispatch(dbconnection, event)

def sync(lock):
    """
    A thread that will sync Leases with the local rethinkdb
    """
    # db connection is shared between threads
    dbconnection = connect()

    logger = logging.getLogger('myslice.leases')
    while True:
        logger.info("syncing Leases")
        try:
            syncLeases()
        except Exception as e:
            logger.exception(e)
            continue
        logger.info("sleeping")

        # sleep for 5 minutes
        # to be fine tuned
        time.sleep(300)

def syncLeases():
    try:
        logger.debug("Query Lease")
        ll = q(Lease).get()

        logger.debug("syncLeases")
        # syncs leases configured with the db
        slices = db.syncLeases(ll)

        for s in slices:
            logger.info("Synchronize slice %s after syncLeases" % s)
            syncSlices(s)

    except Exception as e:
        #import traceback
        #traceback.print_exc()
        logger.exception("Service does not seem to be available")
        logger.exception(str(e))
        raise

