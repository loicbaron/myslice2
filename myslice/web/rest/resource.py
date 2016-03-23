import json

import rethinkdb as r
from tornado import gen

from myslice.web.rest import Api, DecimalEncoder, DateEncoder


class ResourceHandler(Api):

    @gen.coroutine
    def get(self, resource_id):
        resources = []
        if resource_id:
            item = yield r.table('resources').get(resource_id).run(self.dbconnection)

            if item is None:
                self.set_status(404)
                self.finish({"reason": "Slices not found, Please check the URI."})
            else:
                resources.append(item)
        else:
            cursor = yield r.table('resources').run(self.dbconnection)

            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                resources.append(item)

        self.write(json.dumps({"resources": resources}, cls=DecimalEncoder, default=DateEncoder))