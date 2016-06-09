import json

import rethinkdb as r

from myslice.lib.util import myJSONEncoder
from myslice.db.activity import Event, EventAction, ObjectType
from myslice.web.rest import Api


from tornado import gen, escape

class UsersHandler(Api):

    @gen.coroutine
    def get(self, id):
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

        try:
            data = escape.json_decode(self.request.body)['data']
        except json.decoder.JSONDecodeError as e:
            self.userError("malformed request", e.message)
            return
        print(self.get_current_user_id())
        print("---> REST POST PROJECT")
        import re
        # urn:publicid:IDN+onelab:upmc:test+authority+sa
        u = self.get_current_user_id()
        auth = '+'.join(u.split('+')[:-2])
        id = auth + ':' + data['name'] + '+authority+sa'
        try:
            event = Event({
                'action': EventAction.CREATE,
                'user': self.get_current_user_id(),
                'object': {
                    'type': ObjectType.USER,
                    'id': id,
                },
                'data': data
            })
        except Exception as e:
            self.userError("problem with request", e.message)
            return
        else:
            result = yield dispatch(self.dbconnection, event)
            # data = self.get_argument('event','no data')
            self.write(json.dumps({"result": "ok"}, cls=myJSONEncoder))
            print(event)

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

class ProfileHandler(Api):

    @gen.coroutine
    def get(self):
        """
        GET /profile

        Logged in User Profile

        :return:
        """
        # TODO: id must be a valid URN

        profile = yield r.table('users').get(self.get_current_user_id).run(self.dbconnection)

        self.write(json.dumps({"result": profile}, cls=myJSONEncoder))
