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
from myslicelib.model.resource import Resource
from myslicelib.query import q

logger = logging.getLogger('myslice.service.resources')

def sync(lock):
    """
    A thread that will sync resources with the local rethinkdb
    """

    # DB connection
    dbconnection = connect()

    while True:
        # acquires lock
        with lock:
            logger.info("Worker resources starting synchronization")

            # MySliceLib Query Slices
            p = q(Resource).get()

            # update local resources table
            lresources = db.resources(dbconnection, p.dict())

            for ls in lresources :
                # add status if not present and update on db
                if not 'status' in ls:
                    ls['status'] = Status.ENABLED
                    ls['enabled'] = format_date()
                    db.resources(dbconnection, ls)

                if not p.has(ls['id']) and ls['status'] is not Status.PENDING:
                    # delete resources that have been deleted elsewhere
                    db.delete(dbconnection, 'resources', ls['id'])
                    logger.info("Project {} deleted".format(ls['id']))

        # sleep
        time.sleep(86400)


