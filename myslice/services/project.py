import logging
import myslice.db as db
from myslice.lib import Status
from myslice.lib.util import format_date

from myslicelib.model.project import Project
from myslicelib.query import q

logger = logging.getLogger('myslice.service.projects')

def run():
    """
    A thread that will check resource availability and information
    """
    logger.info("Process projects starting")

    """
    DB connection
    """
    dbconnection = db.connect()

    """
    MySliceLib Query Slices
    """
    projects = q(Project).get()

    """
    update local slice table
    """
    lprojects = db.projects(dbconnection, projects.dict())

    for lp in lprojects :
        if not projects.has(lp['id']) and lp['status'] is not Status.PENDING:
            # delete resourc that have been deleted elpewhere
            db.delete(dbconnection, 'projects', lp['id'])
            logger.info("Project {} deleted".format(lp['id']))

        # add status if not present and update on db
        if not 'status' in lp:
            lp['status'] = Status.ENABLED
            lp['enabled'] = format_date()
            db.projects(dbconnection, lp)
