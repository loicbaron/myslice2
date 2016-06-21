import json
from email.utils import parseaddr
import crypt
from hmac import compare_digest as compare_hash

import rethinkdb as r
from myslice.db import dispatch, changes
from myslice.lib.util import myJSONEncoder
from myslice.db.activity import Event, EventAction, ObjectType
from myslice.db import dispatch
from myslice.web.rest import Api

from tornado import gen, escape

class LoginHandler(Api):

    @gen.coroutine
    def post(self):
        """
        POST /login
        { email: <email>, password: <password> }
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

        if not data['email']:
            self.userError("Email not specified")
            return

        if not data['password']:
            self.userError("Password not specified")
            return
        else:
            password = data['password']

        _, email = parseaddr(data['email'])
        if not email:
            self.userError("Wrong Email address")
            return

        feed = yield r.table('users').filter({"email": email}).run(self.application.dbconnection)
        yield feed.fetch_next()
        user = yield feed.next()

        if not user:
            self.userError("User does not exists")
            return

        p = bytes(password, 'latin-1')

        #self.userError("{}".format(p))

        cpassword = crypt.crypt(str(p), user['password'][:12])
        if not compare_hash(cpassword, user['password']):
            self.userError("password does not match {} - {}".format(cpassword, user['password']))
            return

        # TODO: integrate OAuth2 and pass a token to the user
        self.set_current_user(user['id'])

        self.write(json.dumps(
                {
                    "result": "success",
                    "error": None,
                    "debug": None
                }, cls=myJSONEncoder))

        # TODO: Maybe create a log event when logging in?
        # try:
        #     event = Event({
        #         'action': EventAction.CREATE,
        #         'user': self.get_current_user_id(),
        #         'object': {
        #             'type': ObjectType.USER
        #         },
        #         'data': data
        #     })
        # except Exception as e:
        #     self.userError("Can't create request", e.message)
        #     return
        # else:
        #     result = yield dispatch(self.dbconnection, event)
        #     print(result)
        #     self.write(json.dumps(
        #         {
        #             "result": "success",
        #             "error": None,
        #             "debug": None
        #         }, cls=myJSONEncoder))


class UsersHandler(Api):

    @gen.coroutine
    def get(self, id=None, o=None):

        """
            GET /users/[<id>[/(projects)]]

            User list or user with <id>
            User or Slice list part of project with <id>

            :return:
            """

        user = None
        response = []

        if id:
            # get the user
            cursor = yield r.table('users').get(id).run(self.dbconnection)

            while (yield cursor.fetch_next()):
                user = yield cursor.next()

            if not user:
                self.userError("no user found or permission denied")
                return

            # GET /users/<id>/projects
            if o == 'projects':
                # users in a project
                cursor = yield r.table('projects').filter(lambda project:
                                                       project["pi_users"].contains(id)
                                                       ).run(self.dbconnection)
                while (yield cursor.fetch_next()):
                    item = yield cursor.next()
                    response.append(item)

            # GET /users/<id>/slices
            if o == 'slices':
                # users in a project
                cursor = yield r.table('slices').filter(lambda project:
                                                          project["users"].contains(id)
                                                          ).run(self.dbconnection)
                while (yield cursor.fetch_next()):
                    item = yield cursor.next()
                    response.append(item)

            # GET /users/<id>
            elif o is None:
                response.append(user)

            else:
                self.userError("invalid request")
                return

        # GET /users
        else:
            # list of users
            cursor = yield r.table('users').run(self.dbconnection)

            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                response.append(item)

        self.write(json.dumps({"result": response}, cls=myJSONEncoder))

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

        print('posted')

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
