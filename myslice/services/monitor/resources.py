from myslicelib.model.resource import Resource
from myslicelib.query import q

def run():
    """
    Monitor Resources status (Availability)

    :return:
    """

    #resources = q(Resource).get()

    #for r in resources:
    #    print(r.name)

    pass

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
