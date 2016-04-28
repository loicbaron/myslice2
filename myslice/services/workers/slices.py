##
#   MySlice version 2
#
#   Slices thread workers
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##

import logging
import time
import myslice.db as db
from myslice.lib import Status
from myslice.lib.util import format_date

from myslice.db.activity import Event, ObjectType
from myslice.db import changes, connect
from myslicelib.model.lease import Lease
from myslicelib.model.resource import Resource
from myslice.db.project import Project
from myslice.db.slice import Slice
from myslice.db.user import User
from myslicelib.query import q

logger = logging.getLogger('myslice.service.experiments')

def events_run(lock, qSliceEvents):
    """
    Process the authority after approval 
    """

    logger.info("Worker authorities events starting") 

    # db connection is shared between threads
    dbconnection = connect()

    while True:

        try:
            event = Event(qSliceEvents.get())
        except Exception as e:
            logger.error("Problem with event: {}".format(e))
        else:
            logger.info("Processing event from user {}".format(event.user))
            
            with lock:
                try:
                    event.setRunning()

                    if event.creatingObject() or event.updatingObject():
                        s = Slice(event.object.data)
                        s.id = event.object.id 
                        # TODO: Registry Only
                        # TODO: Do we add the event.user to the slice???
                        result = s.save()

                    if event.deletingObject():
                        # TODO: Registry Only
                        result = q(Slice).id(event.object.id).delete()

                    if event.addingObject():
                        s = Slice(db.get(dbconnection, table='slices', id=event.object.id))

                        # TODO: Registry Only
                        if event.data['type'] == ObjectType.USER:
                            for val in event.data['values']:
                                u = User(db.get(dbconnection, table='users', id=val))
                                s.addUser(u)
                            result = s.save()

                        # TODO: AMs Only / Filter list of AMs based on the resources
                        if event.data['type'] == ObjectType.RESOURCE:
                            # "values": [{id:"YYYYYY",lease:{start_time:xxxx, end_time:xxxx}}, {id:“ZZZZZZ”}]
                            for val in event.data['values']:
                                r = Resource(db.get(dbconnection, table='resources', id=val['id']))
                                s.addResource(r)
                                if 'lease' in val:
                                    l = Lease(val['lease'])
                                    l.addResource(r)
                                s.addLease(l)
                            result = s.save()

                    if event.removingObject():
                        s = Slice(db.get(dbconnection, table='slices', id=event.object.id))

                        # TODO: Registry Only
                        if event.data['type'] == ObjectType.USER:
                            for val in event.data['values']:
                                u = User(db.get(dbconnection, table='users', id=val))
                                s.removeUser(u)
                            result = s.save()

                        # TODO: AMs Only / Filter list of AMs based on the resources
                        if event.data['type'] == ObjectType.RESOURCE:
                            # "values": [{id:"YYYYYY",lease:{start_time:xxxx, end_time:xxxx}}, {id:“ZZZZZZ”}]
                            for val in event.data['values']:
                                r = Resource(db.get(dbconnection, table='resources', id=val['id']))
                                s.removeResource(r)
                                if 'lease' in val:
                                    l = Lease(val['lease'])
                                    l.removeResource(r)
                                s.addLease(l)
                            result = s.save()

                except Exception as e:
                    logger.error("Problem with event: {}".format(e))
                    result = None
                    event.logError(str(e))
                    event.setError()
                     
                if result:
                    print(result)
                    db.projects(dbconnection, result, event.object.id)
                    event.setSuccess()
                
                db.dispatch(dbconnection, event)

def sync(lock):
    """
    A thread that will sync projects with the local rethinkdb
    """

    # DB connection
    dbconnection = db.connect()

    # XXX ATTENTION !!!
    # TODO: How to synchronize the resources for each Slice???

    while True:
        with lock:
            logger.info("Worker slices starting synchronization")

            # MySliceLib Query Slices
            slices = q(Slice).get()

            # update local slice table
            lslices = db.slices(dbconnection, slices.dict())

            for ls in lslices :
                if not slices.has(ls['id']) and ls['status'] is not Status.PENDING:
                    # delete slices that have been deleted elsewhere
                    db.delete(dbconnection, 'slices', ls['id'])
                    logger.info("Slice {} deleted".format(ls['id']))

                # add status if not present and update on db
                if not 'status' in ls:
                    ls['status'] = Status.ENABLED
                    ls['enabled'] = format_date()
                    db.slices(dbconnection, ls)

        # sleep
        time.sleep(86400)
