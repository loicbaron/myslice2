import time
import logging
import myslice.db as db
from myslicelib.model.testbed import Testbed
from myslicelib.query import q

def run():
    """
    Monitor Testbeds status (AM)

    :return:
    """

    logger = logging.getLogger('myslice.monitor.testbeds')

    while True:
        logger.info("syncing")
        try:
            # retreive version and status info from the testbeds
            r = q(Testbed).version()

            # syncs testbeds configured with the db
            db.syncTestbeds(r)

        except Exception as e:
            logger.exception("Service does not seem to be available")

        logger.info("sleeping")
        time.sleep(86400)