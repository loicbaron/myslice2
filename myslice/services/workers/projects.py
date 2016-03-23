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

from myslicelib.model.project import Project
from myslicelib.query import q

logger = logging.getLogger('myslice.service.experiments')

def sync(lock):
    """
    A thread that will sync projects with the local rethinkdb
    """

    # DB connection
    dbconnection = db.connect()

    while True:
        # acquires lock
        with lock:
            logger.info("Worker projects starting synchronization")

            # MySliceLib Query Slices
            projects = q(Project).get()

            # update local projects table
            lprojects = db.projects(dbconnection, projects.dict())

            for lp in lprojects :
                if not projects.has(lp['id']) and lp['status'] is not Status.PENDING:
                    # delete slices that have been deleted elsewhere
                    db.delete(dbconnection, 'projects', lp['id'])
                    logger.info("Project {} deleted".format(lp['id']))

                # add status if not present and update on db
                if not 'status' in lp:
                    lp['status'] = Status.ENABLED
                    lp['enabled'] = format_date()
                    db.projects(dbconnection, lp)

        # sleep
        time.sleep(86400)

