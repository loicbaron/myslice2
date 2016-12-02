##
#   MySlice version 2
#
#   Projects thread workers
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
#            Loïc Baron <loic.baron@lip6.fr>
##

import logging
import time
from pprint import pprint

import myslice.db as db
from myslice.lib import Status
from myslice.lib.util import format_date

from myslice.lib.authentication import UserSetup
from myslice import myslicelibsetup

from myslice.db.activity import Event, ObjectType
from myslice.db import changes, connect
from myslice.db.user import User
from myslicelib.model.lease import Lease
from myslicelib.model.resource import Resource
from myslice.db.slice import Slice, SliceException, SliceWarningException
from myslicelib.query import q

logger = logging.getLogger('myslice.services.workers.leases')

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
        else:
            logger.info("Processing event from user {}".format(event.user))
            try:
                event.setRunning()
                isSuccess = False

                u = User(db.get(dbconnection, table='users', id=event.user))
                user_setup = UserSetup(u, myslicelibsetup.endpoints)

                if event.creatingObject(): 
                    lease = Lease(event.data)
                    sli = Slice(db.get(dbconnection, table='slices', id=event.data['slice_id']))
                    if not sli:
                        raise Exception("Slice doesn't exist")

                    for val in event.data['resources']:
                        r = db.get(dbconnection, table='resources', id=val)
                        # Add resource only if it exists in DB
                        print("Resource r")
                        pprint(r)
                        print(type(r))
                        if r is not None:
                            r = Resource(r)
                            print("add resource r")
                            sli.addResource(r)
                        else:
                            print("-"*10)
                            print("R do not exist")
                            r = Resource({'id':val})
                            lease.removeResource(r)
                            pprint(lease)
                            print("-"*10)

                    if len(lease.resources) > 0:
                        sli.addLease(lease)
                    else:
                        raise Exception("Invalid resources")
                    print("workers lease slice = ")
                    pprint(sli)
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
                    event.logError(str(err))
                # XXX TO BE REFINED
                event.setError()

            except SliceWarningException as e:
                for err in e.stack:
                    event.logError(str(err))
                event.setWarning()

            except Exception as e:
                import traceback
                traceback.print_exc()
                logger.error("Problem with event: {}".format(e))
                event.logError(str(e))
                event.setError()
            else:
                if isSuccess:
                    event.setSuccess()
                else:
                    event.setError()
            db.dispatch(dbconnection, event)

def sync(lock):
    """
    A thread that will sync Leases with the local rethinkdb
    """
    # db connection is shared between threads
    dbconnection = connect()

    logger = logging.getLogger('myslice.leases')
    print ("Sync leases")
    while True:
        logger.info("syncing Leases")
        try:
            print("Query Lease")
            ll = q(Lease).get()
            print("End Query")

            # syncs leases configured with the db
            db.syncLeases(ll)

            for l in ll:
                if hasattr(l, 'slice_id'):
                    print("Synchronize slice %s" % l.slice_id)
                    logger.info("Synchronize slice %s" % l.slice_id)
                    # if the slice is part of the portal
                    print("db get slices")
                    tmp = db.get(dbconnection, table='slices', id=l.slice_id)
                    print(tmp)
                    if db.get(dbconnection, table='slices', id=l.slice_id):
                        print("it should sync")
                        pprint(l)
                        syncSlices(l.slice_id)

        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.exception("Service does not seem to be available")
            logger.exception(str(e))

        logger.info("sleeping")

        # sleep for 5 minutes
        # to be fine tuned
        time.sleep(300)
