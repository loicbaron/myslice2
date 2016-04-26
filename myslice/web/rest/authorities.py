import json

import rethinkdb as r

from myslice.lib.util import myJSONEncoder
from myslice.web.rest import Api

from tornado import gen, escape

class AuthoritiesHandler(Api):

    @gen.coroutine
    def get(self):
        """
        GET /authorities/[<id>]

        User list or user with <id>

        :return:
        """

        authorities = []

        # TODO: id must be a valid URN
        if id:
            result = yield r.table('authorities').get(id).run(self.dbconnection)
            authorities.append(result)
        else:
            cursor = yield r.table('authorities').run(self.dbconnection)

            while (yield cursor.fetch_next()):
                result = yield cursor.next()
                authorities.append(result)

        self.write(json.dumps({"result": authorities}, cls=myJSONEncoder))

    @gen.coroutine
    def post(self):
        """
        POST /authorities
        :return:
        """
        pass

    @gen.coroutine
    def put(self):
        """
        PUT /authorities/<id>
        :return:
        """
        pass

    @gen.coroutine
    def delete(self):
        """
        DELETE /authorities/<id>
        :return:
        """
        pass