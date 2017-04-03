##
#   MySlice version 2
#
#   Slices thread workers
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##

import json
import time
import threading

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

import myslice.lib.log as logging

##
# lock shared byt the two workers sync and manage
lock = threading.Lock()

logger = logging.getLogger("experiments")

# db connection is shared between threads
dbconnection = connect()


def events_run(qSliceEvents):
    """
    Process the slice after approval 
    """

    logger.info("Worker slices events starting") 

    while True:

        try:
            event = Event(qSliceEvents.get())
        except Exception as e:
            logger.error("Problem with event: {}".format(e))
            event.logError(str(e))
            event.setError()
            dispatch(dbconnection, event)
        else:
            logger.info("Processing event {} from user {}".format(event.id, event.user))
            
            with lock:
                try:
                    event.setRunning()
                    isSuccess = False

                    u = User(db.get(dbconnection, table='users', id=event.user))
                    user_setup = UserSetup(u, myslicelibsetup.endpoints)

                    if event.creatingObject(): 
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
                        # Take into account the Resources on Create
                        if 'resources' in event.data:
                            for resource in event.data['resources']:
                                if not isinstance(resource, dict):
                                    res = db.get(dbconnection, table='resources', id=resource)
                                    if not res:
                                        raise Exception("Resource %s doesn't exist" % resource)
                                    resource = res
                                sli.addResource(Resource(resource))
                        # expiration_date = Renew at AMs
                        isSuccess = sli.save(dbconnection, user_setup)

                    if event.updatingObject():
                        logger.debug("Update users / resources of Slice %s" % event.object.id)
                        sli = Slice(db.get(dbconnection, table='slices', id=event.object.id))

                        ## adding users
                        sli = add_users(event.data, sli)

                        ## removing users
                        sli = remove_users(event.data, sli)

                        ## adding resources
                        sli = add_resources(event.data, sli)

                        ## removing resources
                        sli = remove_resources(event.data, sli)

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
                                res = Resource(db.get(dbconnection, table='resources', id=val))
                                sli.addResource(res)
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

def add_users(data, slice):
    # check if the users in the request are in the slice
    for data_user in data['users']:
        if isinstance(data_user, dict):
            u = User(data_user)
        else:
            u = User(db.get(dbconnection, table='users', id=data_user))
        if u.id not in slice.users:
            slice.addUser(u)
    return slice

def remove_users(data, slice):
    data_users = [d['id'] if isinstance(d,dict) else d for d in data['users']]
    # check if we need to remove users from the slice
    for user_id in slice.users:
        if user_id not in data_users:
            # remove user from slice
            u = User(db.get(dbconnection, table='users', id=user_id))
            slice.removeUser(u)
    return slice

def add_resources(data, slice):
    # check if the resources in the request are in the slice
    for data_resource in data['resources']:
        if isinstance(data_resource, dict):
            res = Resource(data_resource)
        else:
            res = Resource(db.get(dbconnection, table='resources', id=data_resource))
        if res.id not in [x['id'] for x in slice.resources]:
            slice.addResource(res)
    return slice

def remove_resources(data, slice):
    data_resources = [d['id'] if isinstance(d,dict) else d for d in data['resources']]
    # check if we need to remove resources from the slice
    for resource_id in [x['id'] for x in slice.resources]:
        if resource_id not in data_resources:
            # remove resource from slice
            res = Resource(db.get(dbconnection, table='resources', id=resource_id))
            slice.removeUser(res)
    return slice

def sync():
    """
    A thread that will sync slices with the local rethinkdb
    """
    while True:
        syncSlices()
        # sleep
        time.sleep(86400)

def syncSlices(id=None):

    with lock:
        logger.info("Worker slices starting synchronization")
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

            # ------------------------------------------------------
            # Synchronize resources of a Slice at AMs
            # !!! only if the slice_id is specified !!!
            # Otherwise it is way too long to synchronize all slices
            # ------------------------------------------------------
            # TODO: trigger this function in background for a user
            # that want to refresh his slice / when he selected one
            # ------------------------------------------------------
            if id:
                for slice in slices:
                    if len(slice.users) > 0:
                        try:
                            u = User(db.get(dbconnection, table='users', id=slice.users[0]))

                            logger.info("Synchronize slice %s:" % slice.hrn)

                            # Synchronize resources of the slice only if we have the user's private key or its credentials
                            # XXX Should use delegated Credentials
                            #if (hasattr(u,'private_key') and u.private_key is not None and len(u.private_key)>0) or (hasattr(u,'credentials') and len(u.credentials)>0):
                            if u.private_key or (hasattr(u,'credentials') and len(u.credentials)>0):
                                user_setup = UserSetup(u,myslicelibsetup.endpoints)
                                logger.info("Slice.id(%s).get() with user creds" % slice.hrn)
                                s = q(Slice, user_setup).id(slice.id).get().first()
                                db.slices(dbconnection, s.dict(), slice.id)
                        except Exception as e:
                            import traceback
                            traceback.print_exc()
                            logger.error("Problem with slice %s" % slice.id)
                            logger.exception(str(e))
                    else:
                        logger.info("slice %s has no users" % slice.hrn)

            # update local slice table
            else:
                if len(slices)>0:
                    local_slices = db.slices(dbconnection)
                    # Add slices from Registry unkown from local DB
                    for s in slices:
                        if not db.get(dbconnection, table='slices', id=s.id):
                            logger.info("Found new slice from Registry: %s" % s.id)
                            db.slices(dbconnection, s.dict(), s.id)
                    # Update slices known in local DB
                    for ls in local_slices :
                        logger.info("Synchronize Slice {}".format(ls['id']))
                        # add status if not present and update on db
                        if not 'status' in ls:
                            ls['status'] = Status.ENABLED
                            ls['enabled'] = format_date()
                        if not slices.has(ls['id']) and ls['status'] is not Status.PENDING:
                            # delete slices that have been deleted elsewhere
                            db.delete(dbconnection, 'slices', ls['id'])
                            logger.info("Slice {} deleted".format(ls['id']))
                        else:
                            db.slices(dbconnection, ls, ls['id'])
                else:
                    logger.warning("Query slices is empty, check myslicelib and the connection with SFA Registry")

        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.exception(str(e))

        logger.info("Worker slices finished period synchronization")
