##
#   MySlice version 2
#
#   Projects thread workers
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

from myslice.db.activity import Event, ObjectType, DataType
from myslice.db import changes, connect
from myslice.db.user import User
from myslice.db.project import Project
from myslicelib.query import q

logger = logging.getLogger('myslice.service.experiments')

def events_run(lock, qProjectEvents):
    """
    Process the authority after approval 
    """

    logger.info("Worker authorities events starting") 

    # db connection is shared between threads
    dbconnection = connect()

    isSuccess = None

    while True:

        try:
            event = Event(qProjectEvents.get())
        except Exception as e:
            logger.error("Problem with event: {}".format(e))
        else:
            logger.info("Processing event from user {}".format(event.user))

            with lock:
                try:
                    event.setRunning()
                    isSuccess = False

                    if event.creatingObject() or event.updatingObject():
                        logger.info("creating or updating the object project {}".format(event.object.id)) 
                        
                        proj = Project(event.data)
                        proj.id = event.object.id
                        pi = User(db.get(dbconnection, table='users', id=event.user))
                        proj.addPi(pi) 
                        # TODO: Registry Only
                        isSuccess = proj.save(dbconnection)

                    if event.deletingObject():
                        logger.info("deleting the object project {}".format(event.object.id)) 

                        proj = Project(db.get(dbconnection, table='projects', id=event.object.id))
                        if not proj:
                            raise Exception("Projects doesn't exist")
                        isSuccess = proj.delete(dbconnection)

                    if event.addingObject():
                        logger.info("adding data to the object project {}".format(event.object.id)) 

                        if event.data.type == DataType.USER:
                            logger.info("Project only supports PI at the moment, need new feature in SFA Reg")
                        if event.data.type == DataType.PI or event.data.type == DataType.USER:
                            proj = Project(db.get(dbconnection, table='projects', id=event.object.id))
                            for val in event.data.values:
                                pi = User(db.get(dbconnection, table='users', id=val))
                                proj.addPi(pi)
                            isSuccess = proj.save(dbconnection)

                    if event.removingObject():
                        logger.info("removing data from the object project {}".format(event.object.id)) 

                        if event.data.type == DataType.USER:
                            logger.info("Project only supports PI at the moment, need new feature in SFA Reg")
                        if event.data.type == DataType.PI or event.data.type == DataType.USER:
                            proj = Project(db.get(dbconnection, table='projects', id=event.object.id))
                            for val in event.data.values:
                                pi = User(db.get(dbconnection, table='users', id=val))
                                proj.removePi(pi)
                            isSuccess = proj.save(dbconnection)

                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    logger.error("Problem with event: {}".format(e))
                    event.logError(str(e))

                if isSuccess:
                    event.setSuccess()
                else:
                    event.setError()
                
                db.dispatch(dbconnection, event)

def sync(lock):
    """
    A thread that will sync projects with the local rethinkdb
    """

    # DB connection
    dbconnection = connect()

    while True:
        # acquires lock
        with lock:
            logger.info("Worker projects starting synchronization")

            # MySliceLib Query Slices
            p = q(Project).get()

            # update local projects table
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

        # sleep
        time.sleep(86400)


