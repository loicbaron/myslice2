import json

import rethinkdb as r
from tornado import gen

from myslice.web.rest import Api, DecimalEncoder, DateEncoder


class ResourceHandler(Api):

    @gen.coroutine
    def get(self, *args):
        resources = []

        cursor = yield r.table('resources').run(self.dbconnection)

        while (yield cursor.fetch_next()):
            item = yield cursor.next()
            resources.append(item)

        #self.finish()
        #id = self.get_argument("id")
        #value = self.get_argument("value")
        #data = {"id": id, "value" : value}

        #self.write({"resources": resources})
        self.write(json.dumps({"resources": resources}, cls=DecimalEncoder, default=DateEncoder))

        #for c in cl:
        #    c.write_message(data)