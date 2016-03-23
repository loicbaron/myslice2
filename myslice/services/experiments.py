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


    # update slice table
    #lslices = db.slices(dbconnection, slices.dict())

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