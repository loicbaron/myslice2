import time
import logging
import myslice.db as db
from myslicelib.model.lease import Lease
from myslicelib.query import q

def run():
    """
    Monitor Leases

    :return:
    """

    logger = logging.getLogger('myslice.monitor.leases')
    print ("monitor leases")
    while True:
        logger.info("syncing")
        try:

            ll = q(Lease).get()

            # syncs leases configured with the db
            db.syncLeases(ll)

        except Exception as e:
            logger.exception("Service does not seem to be available")

        logger.info("sleeping")
        print("syn4")
        time.sleep(86400)