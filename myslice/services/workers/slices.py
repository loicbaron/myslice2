##
#   MySlice version 2
#
#   Slices thread workers
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##


import logging
import time
import myslice.db as db
from myslice.lib import Status
from myslice.lib.util import format_date

from myslicelib.model.slice import Slice
from myslicelib.query import q

logger = logging.getLogger('myslice.service.experiments')

def sync(lock):
    """
    A thread that will sync projects with the local rethinkdb
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
                if not slices.has(ls['id']) and ls['status'] is not Status.PENDING:
                    # delete slices that have been deleted elsewhere
                    db.delete(dbconnection, 'slices', ls['id'])
                    logger.info("Slice {} deleted".format(ls['id']))

                # add status if not present and update on db
                if not 'status' in ls:
                    ls['status'] = Status.ENABLED
                    ls['enabled'] = format_date()
                    db.slices(dbconnection, ls)

        # sleep
        time.sleep(86400)