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

import myslice.db as db
from myslice.lib import Status
from myslice.lib.util import format_date

from myslice.lib.authentication import UserSetup
from myslice import myslicelibsetup

from myslice.db.activity import Event, ObjectType, DataType
from myslice.db import changes, connect
from myslicelib.model.lease import Lease
from myslicelib.model.resource import Resource
from myslice.db.slice import Slice, SliceException
from myslicelib.model.slice import Slices
from myslice.db.user import User
from myslicelib.query import q

logger = logging.getLogger('myslice.services.workers.experiments')

def events_run(lock, qSliceEvents):
    """
    Process the slice after approval 
    """

    logger.info("Worker slices events starting") 

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
                    isSuccess = False

                    u = User(db.get(dbconnection, table='users', id=event.user))
                    user_setup = UserSetup(u, myslicelibsetup.endpoints)

                    if event.creatingObject() or event.updatingObject():
                        sli = Slice(event.data)
                        sli.id = event.object.id
                        # Add all Project PIs to the Slice
                        project = db.get(dbconnection, table='projects', id=sli.project)
                        for us in project['pi_users']:
                            us = User(db.get(dbconnection, table='users', id=us))
                            sli.addUser(us)
                        if 'users' in event.data and 'geni_users' not in event.data:
                            for u_id in event.data['users']:
                                u = User(db.get(dbconnection, table='users', id=u_id))
                                sli.addUser(u)
                        # Don't take into account the Resources on Create or Update???
                        # expiration_date = Renew at AMs
                        isSuccess = sli.save(dbconnection, user_setup)

                    if event.deletingObject():
                        sli = Slice(db.get(dbconnection, table='slices', id=event.object.id))
                        if not sli:
                            raise Exception("Slice doesn't exist")
                        isSuccess = sli.delete(dbconnection, user_setup)

                    if event.addingObject():
                        sli = Slice(db.get(dbconnection, table='slices', id=event.object.id))

                        if event.data.type == DataType.USER:
                            for val in event.data.values:
                                if isinstance(val, dict):
                                    val = val['id']
                                u = User(db.get(dbconnection, table='users', id=val))
                                sli.addUser(u)
                            isSuccess = sli.save(dbconnection, user_setup)

                        if event.data['type'] == DataType.RESOURCE:
                            for val in event.data.values:
                                if isinstance(val, dict):
                                    val = val['id']
                                r = Resource(db.get(dbconnection, table='resources', id=val))
                                sli.addResource(r)
                            isSuccess = sli.save(dbconnection, user_setup)

                    if event.removingObject():

                        sli = Slice(db.get(dbconnection, table='slices', id=event.object.id))

                        if event.data.type == DataType.USER:
                            for val in event.data['values']:
                                if isinstance(val, dict):
                                    val = val['id']
                                u = User(db.get(dbconnection, table='users', id=val))
                                sli.removeUser(u)
                            isSuccess = sli.save(dbconnection, user_setup)

                        if event.data.type == DataType.RESOURCE:
                            for val in event.data.values:
                                if isinstance(val, dict):
                                    val = val['id']
                                r = Resource(db.get(dbconnection, table='resources', id=val))
                                sli.removeResource(r)
                            isSuccess = sli.save(dbconnection, user_setup)

                except SliceException as e:
                    # CREATE, UPDATE, DELETE
                    # Calls toward Registry
                    # If an AM sends an Error it is not blocking
                    if event.creatingObject() or event.updatingObject() or event.deletingObject():
                        logger.debug("DEBUG services worker slices")
                        for err in e.stack:
                            logger.debug(err)
                            if err['type'] == 'Reg':
                                event.setError()
                                break
                            else:
                                # XXX TO BE REFINED
                                event.setSuccess()
                                #event.setWarning()
                    # TODO:
                    # if ALL AMs have failed -> Error
                    # if One AM succeeded -> Warning
                    else:
                        # XXX TO BE REFINED
                        logger.debug("DEBUG services worker slices")
                        for err in e.stack:
                            logger.debug(err)
                        event.setWarning()
                        #event.setError()

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
    A thread that will sync slices with the local rethinkdb
    """

    # DB connection
    dbconnection = db.connect()

    while True:
        with lock:
            logger.info("Worker slices starting synchronization")
            syncSlices()
        # sleep
        time.sleep(86400)

def syncSlices(id=None):
    try:
        # DB connection
        dbconnection = db.connect()

        # Update an existing Slice
        if id:
            slices = Slices([Slice(db.get(dbconnection, table='slices', id=id))])
        # MySliceLib Query Slices
        else:
            slices = q(Slice).get()

        if len(slices)==0:
            logger.warning("Query slices is empty, check myslicelib and the connection with SFA Registry")

        for slice in slices:
            if len(slice.users) > 0:
                try:
                    u = User(db.get(dbconnection, table='users', id=slice.users[0]))

                    # Synchronize resources of the slice only if we have the user's private key or its credentials
                    # XXX Should use delegated Credentials
                    #if (hasattr(u,'private_key') and u.private_key is not None and len(u.private_key)>0) or (hasattr(u,'credentials') and len(u.credentials)>0):
                    if u.private_key or (hasattr(u,'credentials') and len(u.credentials)>0):
                        user_setup = UserSetup(u,myslicelibsetup.endpoints)
                        s = q(Slice, user_setup).id(slice.id).get()
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    logger.error("Problem with slice %s" % slice.id)
            else:
                logger.info("slice %s has no users" % slice.hrn)

        # update local slice table
        if not id:
            # update local slice table
            if len(slices)>0:
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
            else:
                logger.warning("Query slices is empty, check myslicelib and the connection with SFA Registry")

    except Exception as e:
        import traceback
        traceback.print_exc()
