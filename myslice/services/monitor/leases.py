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
            print("syn1")
            ll = q(Lease).get()
            print("syn2")
            # syncs leases configured with the db
            db.syncLeases(ll)
            print("syn3")
        except Exception as e:
            logger.exception("Service does not seem to be available")

        logger.info("sleeping")
        print("syn4")
        time.sleep(86400)