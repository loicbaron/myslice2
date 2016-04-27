##
#   MySlice version 2
#
#   Projects thread workers
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

                    if event.creatingObject() or event.updatingObject():
                        a = Project(event.object.data)
                        a.id = event.object.id 
                        result = a.save()

                    if event.deletingObject():
                        result = q(Project).id(event.object.id).delete()

                    if event.addingObject():
                        if event.data['type'] == ObjectType.USER:
                            logger.info("Project only supports PI at the moment, need new feature in SFA Reg")
                        if event.data['type'] == ObjectType.PI or event.data['type'] == ObjectType.USER:
                            a = Project(db.get(dbconnection, table='projects', id=event.object.id))
                            for val in event.data['values']:
                                pi = User(db.get(dbconnection, table='users', id=val))
                                a.addPi(pi)
                            result = a.save()

                    if event.removingObject():
                        if event.data['type'] == ObjectType.USER:
                            logger.info("Project only supports PI at the moment, need new feature in SFA Reg")
                        if event.data['type'] == ObjectType.PI or event.data['type'] == ObjectType.USER:
                            a = Project(db.get(dbconnection, table='projects', id=event.object.id))
                            for val in event.data['values']:
                                pi = User(db.get(dbconnection, table='users', id=val))
                                a.removePi(pi)
                            result = a.save()

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
    dbconnection = connect()

    while True:
        # acquires lock
        with lock:
            logger.info("Worker projects starting synchronization")

            # MySliceLib Query Slices
            p = q(Project).get()

            # update local projects table
            lprojects = db.projects(dbconnection, p.dict())

            for ls in lsrojects :
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


