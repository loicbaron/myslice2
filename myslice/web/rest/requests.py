import json

import rethinkdb as r
from tornado import gen, escape

from myslice.web.rest import Api
from myslice.lib.util import DecimalEncoder, DateEncoder
from myslice.db.activity import Request, RequestStatus

class RequestsHandler(Api):

    @gen.coroutine
    def get(self):
        requests = []

        cursor = yield r.table('requests').run(self.dbconnection)

        while (yield cursor.fetch_next()):
            item = yield cursor.next()
            requests.append(item)

        # return status code
        if not requests:
            self.set_status(404)
            self.finish({"reason": "Not found, Please check the URI."})
        else:
            self.write(json.dumps({"requests": requests}, cls=DecimalEncoder, default=DateEncoder))