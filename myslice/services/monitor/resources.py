import time
import logging
from myslicelib.model.resource import Resource
from myslicelib.query import q

from myslice import db as db

def run():
    """
    Monitor Resources status (Availability)

    :return:
    """

    logger = logging.getLogger('myslice.monitor.resources')

    while True:
        logger.info("syncing")
        try:
            # retreive version and status info from the testbeds
            r = q(Resource).get()

            # syncs testbeds configured with the db
            db.syncResources(r)

        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.exception("Service does not seem to be available")

        logger.info("sleeping")
        time.sleep(86400)

#
# def agent(num, input):
#     """
#     A thread that will check resource availability and information
#     """
#     logging.info("Agent %s starting" % num)
#
#     while True:
#         resource = input.get()
#
#         node = Query('Nodes').hostname(resource).execute().first()
#
#         if not node.enabled:
#             print "+=> (%s) %s is not enabled" % (node.boot, node.hostname)
#             availability = 0
#             status = "disabled"
#
#         elif not node.is_running():
#             print "+=> (%s) %s is not running" % (node.boot, node.hostname)
#             availability = 0
#             status = "down"
#         else:
#             # if not r:
#             #     print "+=> (%s) %s is not accessible" % (node.boot, node.hostname)
#             #     availability = 0
#             #     status = "no access"
#             # else :
#             #     print "+=> (%s) %s is ok" % (node.boot, node.hostname)
#             availability = 1
#             status = "up"
#                 #updates info about the node (testing)
#                 # d.info_resource(node.hostname, {
#                 #     #'ipv4' : node.ip(4),
#                 #     'ipv6' : node.ip(6),
#                 # })
#
#         s.update({
#             "hostname": node.hostname,
#             "bootstate": node.boot,
#             "status": status
#         })
#         ''' send OML stream '''
#         # oml.availability(node.hostname, availability)
