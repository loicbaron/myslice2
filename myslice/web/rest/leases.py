import json

import rethinkdb as r
from tornado import gen

from myslice.web.rest import Api
from myslice.lib.util import myJSONEncoder


class LeasesHandler(Api):

    @gen.coroutine
    def get(self, id=None):
        """
        GET /leases

       Leases list

        :return:
        """
        leases = []



        cursor = yield r.table('leases').run(self.dbconnection)

        while (yield cursor.fetch_next()):
            result = yield cursor.next()
            leases.append(result)

        self.write(json.dumps({"result": leases}, cls=myJSONEncoder))