import json

import rethinkdb as r

from myslice.lib.util import myJSONEncoder
from myslice.web.rest import Api

from myslice.db.activity import Event, EventAction, ObjectType
from myslice.db import dispatch

from tornado import gen, escape

class TestbedsHandler(Api):

    @gen.coroutine
    def get(self, id=None, o=None, a=None, b=None):
        """
            - GET /testbeds
                (public) Testbed list

            - GET /testbeds/<id>
                (public) Testbed with <id>

            - GET /testbeds/<id>/(resources)
                (auth) Resource list of the testbed <id>

            - GET /testbeds/<id>/resources?timestamp_start=<XXX>&timestamp_end=<XXX>
                (auth) Resource list of the testbed <id> that are available within a time range

            - GET /testbeds/<id>/leases
                Leases list of the testbed with the <id>

            - GET /testbeds/<id>/leases?timestamp_start=<XXX>&timestamp_end=<XXX>
                (auth) Leases list of the testbed <id> within a time range

            :return:
            """

        response = []
        current_user = self.get_current_user()

        # [?timestamp_start=<XXX>&timestamp_end=<XXX>]
        ts = self.get_argument('timestamp_start',None)
        te = self.get_argument('timestamp_end',None)

        # GET /testbeds
        if not id and not o:
            cursor = yield r.table('testbeds') \
                .run(self.dbconnection)
            while (yield cursor.fetch_next()):
                testbed = yield cursor.next()
                response.append(testbed)


        # GET /testbeds/<id>
        elif not o and id and self.isUrn(id):

            cursor = yield r.table('testbeds') \
                .filter({'id': id}) \
                .run(self.dbconnection)
            while (yield cursor.fetch_next()):
                testbed = yield cursor.next()
                response.append(testbed)

        # GET /testbeds/<id>/resources
        elif id and self.isUrn(id) and o == 'resources' and not ts and not te:
            cursor = yield r.table(o) \
                .filter(lambda resource: resource["testbed"] == id) \
                .run(self.dbconnection)

            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                response.append(item)

        # GET /testbeds/<id>/resources?timestamp_start=<XXX>&timestamp_end=<XXX>
        elif id and self.isUrn(id) and o == 'resources':
            # Resources NOT in Leases
            cursor = yield r.table(o) \
                .filter(lambda resource: resource["testbed"] == id) \
                .filter({'available':'true'}) \
                .filter( lambda resource: 
                    r.table("leases").map(lambda l: 
                        l['resources'].coerce_to('array')
                    ).reduce(lambda left, right:
                        left.set_union(right)
                    ).contains(resource['id']).not_() \
                ).run(self.dbconnection)

            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                response.append(item)

            if ts and te:
                # List of Resources ids in Leases but not in the given time range
                in_leases = yield r.table("leases").filter(lambda l:
                    r.or_(l['start_time'].gt(int(te)),l['end_time'].lt(int(ts)))
                ).map(lambda l: 
                    l['resources'].coerce_to('array')
                ).reduce(lambda left, right:
                    left.set_union(right)
                ).map(lambda x: 
                    r.table('resources').get(x)
                ).filter({'testbed':id}).run(self.dbconnection)
                response = response + in_leases

            if ts and not te:
                # List of Resources ids in Leases but not in the given time range
                in_leases = yield r.table("leases").filter(lambda l:
                    l['start_time'].gt(int(te))
                ).map(lambda l: 
                    l['resources'].coerce_to('array')
                ).reduce(lambda left, right:
                    left.set_union(right)
                ).map(lambda x: 
                    r.table('resources').get(x)
                ).filter({'testbed':id}).run(self.dbconnection)
                response = response + in_leases

            if not ts and te:
                # List of Resources ids in Leases but not in the given time range
                in_leases = yield r.table("leases").filter(lambda l:
                    l['end_time'].lt(int(ts))
                ).map(lambda l: 
                    l['resources'].coerce_to('array')
                ).reduce(lambda left, right:
                    left.set_union(right)
                ).map(lambda x: 
                    r.table('resources').get(x)
                ).filter({'testbed':id}).run(self.dbconnection)
                response = response + in_leases

        # GET /testbeds/<id>/leases
        elif id and self.isUrn(id) and o == 'leases' and not ts and not te:
            cursor = yield r.table(o) \
                .filter(lambda ls: ls["testbed"] == id) \
                .run(self.dbconnection)

            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                response.append(item)

        # GET /testbeds/<id>/leases?timestamp_start=<XXX>&timestamp_end=<XXX>
        elif id and self.isUrn(id) and o == 'leases' and ts and te:
            cursor = yield r.table(o) \
                .filter(lambda ls: ls["testbed"] == id) \
                .filter(lambda l:
                    r.and_(l['start_time'].ge(int(ts)),l['end_time'].le(int(te)))
                ).run(self.dbconnection)

            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                response.append(item)

        # GET /testbeds/<id>/leases?timestamp_start=<XXX>
        elif id and self.isUrn(id) and o == 'leases' and ts and not te:
            cursor = yield r.table(o) \
                .filter(lambda ls: ls["testbed"] == id) \
                .filter(lambda l:
                    l['start_time'].ge(int(ts))
                ).run(self.dbconnection)

            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                response.append(item)

        # GET /testbeds/<id>/leases?timestamp_end=<XXX>
        elif id and self.isUrn(id) and o == 'leases' and not ts and te:
            cursor = yield r.table(o) \
                .filter(lambda ls: ls["testbed"] == id) \
                .filter(lambda l:
                    l['end_time'].le(int(te))
                ).run(self.dbconnection)

            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                response.append(item)
        else:
            self.userError("invalid request")
            return
        self.finish(json.dumps({"result": response}, cls=myJSONEncoder))
