##
# Endpoints worker: will keep the list of endpoints configured in sync
# will also check status and info

import logging
from datetime import datetime
import myslice.db as db

from myslicelib.model.testbed import Testbed
from myslicelib.query import q

logger = logging.getLogger('myslice.worker.endpoints')

def run():
    """
    A thread that will check resource availability and information
    """
    logger.info("Agent endpoints starting")

    """
    DB connection
    """
    dbconnection = db.connect()

    """
    MySliceLib Query Testbeds
    """
    testbeds = q(Testbed).get()
    print(testbeds.dict())

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