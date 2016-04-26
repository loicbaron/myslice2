##
#   MySlice version 2
#
#   Projects thread workers
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##

import logging
import time
from myslice.db import connect, delete, projects
from myslice.db.activity import Event, ObjectType
from myslice.lib import Status
from myslice.lib.util import format_date

from myslicelib.model.project import Project
from myslicelib.query import q

logger = logging.getLogger('myslice.service.experiments')

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
            lprojects = projects(dbconnection, p.dict())

            for lp in lprojects :
                if not p.has(lp['id']) and lp['status'] is not Status.PENDING:
                    # delete slices that have been deleted elsewhere
                    delete(dbconnection, 'projects', lp['id'])
                    logger.info("Project {} deleted".format(lp['id']))

                # add status if not present and update on db
                if not 'status' in lp:
                    lp['status'] = Status.ENABLED
                    lp['enabled'] = format_date()
                    projects(dbconnection, lp)

        # sleep
        time.sleep(86400)

def manageProjects(lock, q):
    """
        Manages newly created events
        """
    logger.info("Worker manage projects starting")

    # db connection is shared between threads
    dbconnection = connect()

    while True:
        try:
            event = Event(q.get())
        except Exception as e:
            logger.error("Problem with event: {}".format(e))
        else:
            with lock:
                # set the event status on running
                event.running()

                # retrieve user who initiated the event

                if event.isRequest() and event.isApproved():
                    # manages the request and
                    # will create a new project
                    pass

                elif event.addingObject():
                    if event.object.type == ObjectType.USER:
                        # adding user to project
                        pass

                elif event.removingObject():
                    if event.object.type == ObjectType.USER:
                        # removing user from project
                        pass
                    if event.object.type == ObjectType.PROJECT:
                        # delete project
                        pass
