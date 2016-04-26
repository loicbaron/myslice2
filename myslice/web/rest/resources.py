import json

import rethinkdb as r
from tornado import gen

from myslice.web.rest import Api
from myslice.lib.util import myJSONEncoder


class ResourcesHandler(Api):

    @gen.coroutine
    def get(self, id=None):
        """
        GET /resources/[<id>]

        Resource list or resource with <id>

        :return:
        """
        resources = []

        # TODO: id must be a valid URN
        if id:
            result = yield r.table('resources').get(id).run(self.dbconnection)
            resources.append(result)
        else:
            cursor = yield r.table('resources').run(self.dbconnection)

            while (yield cursor.fetch_next()):
                result = yield cursor.next()
                resources.append(result)

        self.write(json.dumps({"result": resources}, cls=myJSONEncoder))