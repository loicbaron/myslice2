import json

import rethinkdb as r
from tornado import gen

from myslice.web.rest import Api
from myslice.lib.util import myJSONEncoder


class LeasesHandler(Api):
    @gen.coroutine
    def get(self, o=None):
        """
         GET /leases
         GET /leases/start_time
       Leases list

        :return:
        """
        leases = []

        if not o:
            cursor = yield r.table('leases').run(self.dbconnection)

            while (yield cursor.fetch_next()):
                result = yield cursor.next()
                leases.append(result)
        else:
            cursor = yield r.table('leases').filter({'start_time': o}).run(self.dbconnection)

            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                leases.append(item)
        self.write(json.dumps({"result": leases}, cls=myJSONEncoder))
