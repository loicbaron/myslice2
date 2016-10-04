import json

import rethinkdb as r
from tornado import gen

from myslice.web.rest import Api
from myslice.lib.util import myJSONEncoder


class LeasesHandler(Api):
    @gen.coroutine
    def get(self, o=None, t=None):
        """
         GET /leases
         GET /leases/start_time¶end_time
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
            cursor = yield r.table('leases').filter(r.row['start_time'].eq(int(o)) | (r.row['end_time'].eq(int(o)))).run(self.dbconnection)
            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                leases.append(item)
        self.write(json.dumps({"result": leases}, cls=myJSONEncoder))

