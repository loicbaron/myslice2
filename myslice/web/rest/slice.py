import json

import rethinkdb as r
from tornado import gen

from myslice.web.rest import Api, DecimalEncoder, DateEncoder


class SliceHandler(Api):

    @gen.coroutine
    def get(self, *args):
        resources = []

        cursor = yield r.table('slices').run(self.dbconnection)

        while (yield cursor.fetch_next()):
            item = yield cursor.next()
            resources.append(item)

        #self.finish()
        #id = self.get_argument("id")
        #value = self.get_argument("value")
        #data = {"id": id, "value" : value}

        #self.write({"resources": resources})

        self.set_header('Content-Type','application/json')
        self.write(json.dumps({"slices": resources}, cls=DecimalEncoder, default=DateEncoder))

        #for c in cl:
        #    c.write_message(data)