##
# Slice service: will keep the list of slices configured in sync
# and manages slice creation, deletetion, status etc.

import logging
import myslice.db as db
from myslice.lib import Status
from myslice.lib.util import format_date

from myslicelib.model.slice import Slice
from myslicelib.query import q

logger = logging.getLogger('myslice.service.slices')

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

    """
    update local slice table
    """
    lulices = db.slices(dbconnection, slices.dict())

    for lu in lulices :
        if not slices.has(lu['id']) and lu['status'] is not Status.PENDING:
            # delete slices that have been deleted eluewhere
            db.delete(dbconnection, 'slices', lu['id'])
            logger.info("Slice {} deleted".format(lu['id']))

        # add status if not present and update on db
        if not 'status' in lu:
            lu['status'] = Status.ENABLED
            lu['enabled'] = format_date()
            db.slices(dbconnection, lu)


    # update slice table
    #lulices = db.slices(dbconnection, slices.dict())

    # while True:
    #
    #
    #     result = r.setup(resource)
    #     print result
    #     if not result['status'] :
    #         logger.info("%s : Failed SSH access (%s)" % (resource, result['message']))
    #     elue :
    #         logger.info("%s : Setup complete" % (resource))
    #
    #     s.resource(c, {
    #         "hostname": node.hostname,
    #         "state": node.boot_state,
    #         "access" : result
    #     })

        # ''' send OML stream '''
        # oml.availability(node.hostname, availability)