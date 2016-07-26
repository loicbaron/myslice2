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

#
# while True:
#
#     try:
#         nodes = Query('Nodes').peer(None).execute()
#
#         c = s.connect()
#
#         for node in nodes:
#             #site = node.site
#             s.resource(c,
#                 {
#                     "testbed": "ple",
#                     "hostname": node.hostname
#                     # "site": {
#                     #     "id": site.site_id,
#                     #     "name" : site.name,
#                     #     "short": site.abbreviated_name,
#                     #     "login_base": site.login_base
#                     # }
#                 }
#             )
#             input.put(node.hostname)
#
#         #s.resources()
#
#
#
#     except Exception as e:
#         logger.exception("Service does not seem to be available")
#
#     time.sleep(86400)

# t.join()
