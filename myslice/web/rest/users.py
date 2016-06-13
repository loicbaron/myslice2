import json

import rethinkdb as r
from myslice.db import dispatch, changes
from myslice.lib.util import myJSONEncoder
from myslice.db.activity import Event, EventAction, ObjectType
from myslice.db import dispatch
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
            print(id)
            result = yield r.table('users').get(id).run(self.dbconnection)
            users.append(result)
            print(result)
        else:
            cursor = yield r.table('users').run(self.dbconnection)

            while (yield cursor.fetch_next()):
                result = yield cursor.next()
                users.append(result)

        self.write(json.dumps({"result": users}, cls=myJSONEncoder))

    @gen.coroutine
    def post(self, p):
        """
        POST /users
        :return:
        """
        if not self.request.body:
            self.userError("empty request")
            return

        try:
            data = escape.json_decode(self.request.body)
        except json.decoder.JSONDecodeError as e:
            self.userError("Malformed request", e)
            return
        except Exception as e:
            self.userError("Malformed request", e)
            return
        from pprint import pprint
        pprint(data)

        if not data['authority']:
            self.userError("Authority not specified")
            return

        if not data['email']:
            self.userError("Email not specified")
            return

        try:
            event = Event({
                'action': EventAction.CREATE,
                'user': self.get_current_user_id(),
                'object': {
                    'type': ObjectType.USER
                },
                'data': data
            })
        except Exception as e:
            self.userError("Can't create request", e.message)
            return
        else:
            result = yield dispatch(self.dbconnection, event)
            print(result)
            self.write(json.dumps(
                {
                    "result": "success",
                    "error": None,
                    "debug": None
                 }, cls=myJSONEncoder))

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

        profile = yield r.table('users').get(self.get_current_user_id()).run(self.dbconnection)

        self.write(json.dumps({"result": profile}, cls=myJSONEncoder))

    @gen.coroutine
    def put(self):
        """
        PUT /profile

        :return:
        """
        try:
            data = escape.json_decode(self.request.body)['data']
        except json.decoder.JSONDecodeError as e:
            self.userError("malformed request", e.message)
            return
        try:
            event = Event({
                'action': EventAction.UPDATE,
                'user': self.get_current_user_id(),
                'object': {
                    'type': ObjectType.USER,
                    'id': self.get_current_user_id(),
                },
                'data': data
            })
        except Exception as e:
            self.userError("problem with request", e.message)
            return
        else:
            activity = yield dispatch(self.dbconnection, event)

            feed = yield changes(self.dbconnection, 
                            table='activity', 
                            status=['ERROR', 'SUCCESS'], 
                            id = activity['generated_keys'][0]
                            )

            while (yield feed.fetch_next()):
                result = yield feed.next()
                if result['new_val']['status'] == 'SUCCESS':
                    self.finish(json.dumps({"result": result['new_val']}, cls=myJSONEncoder))
                else:
                    self.userError("updated failed", result['new_val'])




