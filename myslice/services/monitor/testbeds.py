import time
import logging
import myslice.db as db
from myslicelib.model.testbed import Testbed
from myslicelib.query import q

logger = logging.getLogger('myslice.monitor.testbeds')

def run():
    """
    Monitor Testbeds status (AM)

    :return:
    """
    while True:
        logger.info("syncing")
        try:
            syncTestbeds()
        except Exception as e:
            logger.exception(e)
            continue
        logger.info("sleeping")
        time.sleep(86400)

def syncTestbeds():
    try:
        # retreive version and status info from the testbeds
        t = q(Testbed).version()

        if len(t)>0:
            # syncs testbeds configured with the db
            db.syncTestbeds(t)
        else:
            logger.warning("Check myslicelib and SFA, q(Testbed).version() returned empty")

    except Exception as e:
        logger.exception("Service does not seem to be available")
        raise


