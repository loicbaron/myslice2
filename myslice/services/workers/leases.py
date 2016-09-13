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
from myslicelib.model.lease import Lease
from myslicelib.query import q

logger = logging.getLogger('myslice.service.resources')

def sync(lock):
    """
    A thread that will sync leases with the local rethinkdb
    """

    # DB connection
    dbconnection = connect()

    while True:
        # acquires lock
        with lock:
            logger.info("Worker leases starting synchronization")

            # MySliceLib Query Slices

            leases = q(Lease).get()

            # update local leases table
            if len(leases)>0:
                leases = db.leases(dbconnection, leases.dict())
            else:
                logger.warning("Query leases is empty, check myslicelib and the connection with SFA AMs")

            #for ls in lleases :

            #    if CONDITION TBD 
            #        # TBD should we keep the old leases for history or not?
            #        # delete leases that have been deleted elsewhere
            #        db.delete(dbconnection, 'leases', ls['id'])
            #        logger.info("Lease {} deleted".format(ls))


        # sleep
        time.sleep(86400)


