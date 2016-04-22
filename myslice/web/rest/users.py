import json

import rethinkdb as r

from myslice.lib.util import myJSONEncoder
from myslice.web.rest import Api

from tornado import gen, escape

class UsersHandler(Api):

    @gen.coroutine
    def get(self):
        """
        GET /users/[<id>]

        User list or user with <id>

        :return:
        """

        users = []

        # TODO: id must be a valid URN
        if id:
            result = yield r.table('users').get(id).run(self.dbconnection)
            users.append(result)
        else:
            cursor = yield r.table('users').run(self.dbconnection)

            while (yield cursor.fetch_next()):
                result = yield cursor.next()
                users.append(result)

        self.write(json.dumps({"result": users}, cls=myJSONEncoder))

    @gen.coroutine
    def post(self):
        """
        POST /users
        :return:
        """
        pass

    @gen.coroutine
    def put(self):
        """
        PUT /users/<id>
        :return:
        """
        pass

    @gen.coroutine
    def delete(self):
        """
        DELETE /users/<id>
        :return:
        """
        pass