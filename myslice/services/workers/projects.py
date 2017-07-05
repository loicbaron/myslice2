##
#   MySlice version 2
#
#   Projects thread workers
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##

import json
import time

from pprint import pprint

import myslice.db as db
from myslice.lib import Status
from myslice.lib.util import format_date

from myslice.lib.authentication import UserSetup
from myslice import myslicelibsetup

from myslice.db.activity import Event, ObjectType, DataType
from myslice.db import changes, connect
from myslice.db.user import User
from myslice.db.project import Project
from myslicelib.query import q
import myslice.lib.log as logging

logger = logging.getLogger("projects")

def events_run(lock, qProjectEvents):
    """
    Process the authority after approval 
    """

    logger.info("Worker authorities events starting") 

    # db connection is shared between threads
    dbconnection = connect()

    while True:

        try:
            event = Event(qProjectEvents.get())
        except Exception as e:
            logger.error("Problem with event: {}".format(e))
            event.logError(str(e))
            event.setError()
            dispatch(dbconnection, event)
        else:
            logger.info("Processing event: {} from user {}".format(event.id, event.user))

            with lock:
                try:
                    if event.isApproved():
                        user_id = event.manager
                    else:
                        user_id = event.user
                    u = User(db.get(dbconnection, table='users', id=user_id))
                    # Registry Only
                    user_setup = UserSetup(u, myslicelibsetup.registry_endpoints)

                    event.setRunning()
                    event.logInfo("Event is running")
                    logger.debug("Event %s is running" % event.id)
                    isSuccess = False

                    if event.creatingObject() or event.updatingObject():
                        logger.info("creating or updating the object project {}".format(event.data)) 

                        proj = Project(event.data)
                        proj.id = event.object.id

                        # XXX CASES TO BE CHECKED
                        if event.user not in proj.pi_users:
                            pi = User(db.get(dbconnection, table='users', id=event.user))
                            proj.addPi(pi)
                        isSuccess = proj.save(dbconnection, user_setup)
                    else:
                        p = db.get(dbconnection, table='projects', id=event.object.id)
                        if not p:
                            raise Exception("Project doesn't exist")
                        proj = Project(p)

                    if event.deletingObject():
                        logger.info("deleting the object project {}".format(event.object.id)) 
                        isSuccess = proj.delete(dbconnection, user_setup)

                    if event.addingObject():
                        logger.info("adding data to the object project {}".format(event.object.id)) 

                        if event.data.type == DataType.USER:
                            logger.info("Project only supports PI at the moment, need new feature in SFA Reg")
                        if event.data.type == DataType.PI or event.data.type == DataType.USER:
                            for val in event.data.values:
                                pi = User(db.get(dbconnection, table='users', id=val))
                                proj.addPi(pi)
                            isSuccess = proj.save(dbconnection, user_setup)

                    if event.removingObject():
                        logger.info("removing data from the object project {}".format(event.object.id)) 

                        if event.data.type == DataType.USER:
                            logger.info("Project only supports PI at the moment, need new feature in SFA Reg")
                        if event.data.type == DataType.PI or event.data.type == DataType.USER:
                            for val in event.data.values:
                                pi = User(db.get(dbconnection, table='users', id=val))
                                proj.removePi(pi)
                            isSuccess = proj.save(dbconnection, user_setup)

                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    logger.error("Problem with event {}: {}".format(event.id,e))
                    event.logError("Error in worker projects: {}, traceback: {}".format(e,traceback.print_exc()))
                    event.setError()
                else:
                    if isSuccess:
                        event.setSuccess()
                        event.logInfo("Event success")
                        logger.debug("Event %s Success" % event.id)
                    else:
                        logger.error("Error event {}: action failed".format(event.id))
                        event.setError()
                        event.logError("Error in worker projects: action failed")
                finally:
                    db.dispatch(dbconnection, event)

def sync(lock):
    """
    A thread that will sync projects with the local rethinkdb
    """
    while True:
        syncProjects(lock)
        # sleep
        time.sleep(86400)

def syncProjects(lock):

    # DB connection
    dbconnection = connect()

    # acquires lock
    with lock:
        logger.info("Worker projects starting synchronization")

        # MySliceLib Query Slices
        p = q(Project).get()

        # update local projects table
        if len(p)>0:
            lprojects = db.projects(dbconnection, p.dict())
            for ls in lprojects :
                # add status if not present and update on db
                if not 'status' in ls:
                    ls['status'] = Status.ENABLED
                    ls['enabled'] = format_date()
                    db.projects(dbconnection, ls)

                if not p.has(ls['id']) and ls['status'] is not Status.PENDING:
                    # delete projects that have been deleted elsewhere
                    db.delete(dbconnection, 'projects', ls['id'])
                    logger.info("Project {} deleted".format(ls['id']))
        else:
            logger.warning("Query projects is empty, check myslicelib and the connection with SFA Registry")
