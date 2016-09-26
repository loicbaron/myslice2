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
                (auth) Resource list of the testbed with <id>

            - GET /testbeds/<id>/leases
                Leases list of the testbed with the <id>
            :return:
            """

        response = []
        current_user = self.get_current_user()

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
        elif id and self.isUrn(id) and o == 'resources':
            cursor = yield r.table(o) \
                .filter(lambda resource: resource["manager"] == id) \
                .run(self.dbconnection)
                #

            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                response.append(item)

        # GET /testbeds/<id>/leases
        elif id and self.isUrn(id) and o == 'leases':
            cursor = yield r.table(o) \
                .filter(lambda ls: ls["manager"] == id) \
                .run(self.dbconnection)
            #

            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                response.append(item)
        # GET /testbeds/<id>/leases/Start-time/End-time
        elif id and a and b and self.isUrn(id) and o == 'leases':
            cursor = yield r.table(o) \
                .filter({"manager": id, "Start_time": a, "End_time" :b }) \
                .run(self.dbconnection)
            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                response.append(item)
        else:
            self.userError("invalid request")
            return
        self.finish(json.dumps({"result": response}, cls=myJSONEncoder))
