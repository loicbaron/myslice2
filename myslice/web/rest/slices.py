import json

import rethinkdb as r

from myslice.lib.util import myJSONEncoder
from myslice.web.rest import Api

from tornado import gen, escape

class SlicesHandler(Api):

    @gen.coroutine
    def get(self, id):
        """
        GET /slices/[<id>]

        Slice list or slice with <id>

        :return:
        """
        slices = []

        # TODO: id must be a valid URN
        if id:
            result = yield r.table('slices').get(id).run(self.dbconnection)
            slices.append(result)
        else:
            cursor = yield r.table('slices').run(self.dbconnection)

            while (yield cursor.fetch_next()):
                result = yield cursor.next()
                slices.append(result)

        self.write(json.dumps({"result": slices}, cls=myJSONEncoder))

    @gen.coroutine
    def post(self):
        """
        POST /slices
        :return:
        """
        pass

    @gen.coroutine
    def put(self):
        """
        PUT /slices/<id>
        :return:
        """
        pass

    @gen.coroutine
    def delete(self):
        """
        DELETE /slices/<id>
        :return:
        """
        pass