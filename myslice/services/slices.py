##
# Slices worker: will keep the list of slices configured in sync

import logging
from datetime import datetime
import myslice.db as db

from myslicelib.model.slice import Slice
from myslicelib.query import q

logger = logging.getLogger('myslice.worker.slices')

def run():
    """
    A thread that will check resource availability and information
    """
    logger.info("Process slices starting")

    """
    DB connection
    """
    dbconnection = db.connect()

    """
    MySliceLib Query Slices
    """
    slices = q(Slice).get()
    db.slices(dbconnection, slices.dict())


    # while True:
    #
    #
    #     result = r.setup(resource)
    #     print result
    #     if not result['status'] :
    #         logger.info("%s : Failed SSH access (%s)" % (resource, result['message']))
    #     else :
    #         logger.info("%s : Setup complete" % (resource))
    #
    #     s.resource(c, {
    #         "hostname": node.hostname,
    #         "state": node.boot_state,
    #         "access" : result
    #     })

        # ''' send OML stream '''
        # oml.availability(node.hostname, availability)