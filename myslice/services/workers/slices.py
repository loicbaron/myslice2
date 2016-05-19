##
#   MySlice version 2
#
#   Slices thread workers
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##

import json
import logging
import time

from pprint import pprint

import myslice.db as db
from myslice.lib import Status
from myslice.lib.util import format_date

from myslice.lib.authentication import UserSetup
from myslice import myslicelibsetup

from myslice.db.activity import Event, ObjectType, DataType
from myslice.db import changes, connect
from myslicelib.model.lease import Lease
from myslicelib.model.resource import Resource
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

                    u = User(db.get(dbconnection, table='users', id=event.user))
                    user_setup = UserSetup(u, myslicelibsetup.endpoints)

                    if event.creatingObject() or event.updatingObject():
                        s = Slice(event.data)
                        s.id = event.object.id
                        s.addUser(u)
                        if 'users' in event.data and 'geni_users' not in event.data:
                            for u_id in event.data['users']:
                                u = User(db.get(dbconnection, table='users', id=u_id))
                                s.addUser(u)
                        # Don't take into account the Resources on Create or Update???
                        # expiration_date = Renew at AMs
                        result = s.save(user_setup)

                    if event.deletingObject():
                        result = q(Slice).id(event.object.id).delete()

                    if event.addingObject():
                        s = Slice(db.get(dbconnection, table='slices', id=event.object.id))

                        if event.data.type == DataType.USER:
                            for val in event.data.values:
                                u = User(db.get(dbconnection, table='users', id=val))
                                s.addUser(u)
                            result = s.save(user_setup)

                        if event.data['type'] == DataType.RESOURCE:
                            # "values": [{id:"YYYYYY",lease:{start_time:xxxx, end_time:xxxx}}, {id:“ZZZZZZ”}]
                            for val in event.data.values:
                                r = Resource(db.get(dbconnection, table='resources', id=val['id']))
                                pprint(r)
                                s.addResource(r)
                                if 'lease' in val:
                                    l = Lease(val['lease'])
                                    l.addResource(r)
                                    s.addLease(l)
                            u = User(db.get(dbconnection, table='users', id=event.user))
                            user_setup = UserSetup(u, myslicelibsetup.endpoints)
                            result = s.save(user_setup)

                    if event.removingObject():
                        s = Slice(db.get(dbconnection, table='slices', id=event.object.id))

                        if event.data.type == DataType.USER:
                            for val in event.data['values']:
                                u = User(db.get(dbconnection, table='users', id=val))
                                s.removeUser(u)
                            result = s.save(user_setup)

                        if event.data.type == DataType.RESOURCE:
                            # "values": [{id:"YYYYYY",lease:{start_time:xxxx, end_time:xxxx}}, {id:“ZZZZZZ”}]
                            for val in event.data.values:
                                r = Resource(db.get(dbconnection, table='resources', id=val['id']))
                                pprint(r)
                                s.removeResource(r)
                                if 'lease' in val:
                                    l = Lease(val['lease'])
                                    l.removeResource(r)
                                s.addLease(l)
                            result = s.save(user_setup)

                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    logger.error("Problem with event: {}".format(e))
                    result = None
                    event.logError(str(e))
                    event.setError()
                     
                if result:
                    if 'errors' in result and len(result['errors'])>0:
                        logger.error("Error: ".format(result['errors']))
                        event.logError(str(result['errors']))
                        event.setError()
                    else:
                        db.slices(dbconnection, result, event.object.id)
                        event.setSuccess()
                
                db.dispatch(dbconnection, event)

def sync(lock):
    """
    A thread that will sync slices with the local rethinkdb
    """

    # DB connection
    dbconnection = db.connect()

    while True:
        with lock:
            logger.info("Worker slices starting synchronization")

            # MySliceLib Query Slices
            slices = q(Slice).get()

            # update local slice table
            lslices = db.slices(dbconnection, slices.dict())

            for ls in lslices :
                # add status if not present and update on db
                if not 'status' in ls:
                    ls['status'] = Status.ENABLED
                    ls['enabled'] = format_date()
                    db.slices(dbconnection, ls)

                if not slices.has(ls['id']) and ls['status'] is not Status.PENDING:
                    # delete slices that have been deleted elsewhere
                    db.delete(dbconnection, 'slices', ls['id'])
                    logger.info("Slice {} deleted".format(ls['id']))

            for slice in slices:
                if len(slice.users) > 0:
                    try:
                        u = User(db.get(dbconnection, table='users', id=slice.users[0]))

                        # Synchronize resources of the slice only if we have the user's private key or its credentials
                        # XXX Should use delegated Credentials
                        if (hasattr(u,'private_key') and len(u.private_key)>0) or (hasattr(u,'credentials') and len(u.credentials)>0):
                            user_setup = UserSetup(u,myslicelibsetup.endpoints)
                            s = q(Slice, user_setup).id(slice.id).get()
                            pprint(s)
                    except Exception as e:
                        import traceback
                        traceback.print_exc()
                        logger.error("Problem with slice %s" % slice.id)
                else:
                    print("slice %s has no users" % slice.hrn)
        # sleep
        time.sleep(86400)