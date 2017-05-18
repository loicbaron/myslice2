import time
import logging
from myslicelib.model.resource import Resource
from myslicelib.query import q

from myslice import db as db

logger = logging.getLogger('myslice.monitor.resources')

def run():
    """
    Monitor Resources status (Availability)

    :return:
    """
    while True:
        logger.info("syncing")
        syncResources()
        logger.info("sleeping")
        time.sleep(86400)

def syncResources():
    try:
        # retreive resources from testbeds
        r = q(Resource).get()

        if len(r)>0:
            # syncs resources configured with the db
            db.syncResources(r)
        else:
            logger.warning("Check myslicelib and SFA, q(Resource).get() returned empty")

    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.exception("Service does not seem to be available")


