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

        try:
            feed = yield r.table('users').filter({"email": email}).run(self.application.dbconnection)
            yield feed.fetch_next()
            user = yield feed.next()

            if not user:
                self.userError("User does not exists")
                return

        except Exception as e:
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
            - GET /users
                (auth) Users list

            - GET /users/<id>
                (auth) User with <id>

            - GET /users/(projects|slices)
                (auth) Projects/Slices list of the authenticated user

            - GET /users/<id>/(projects|slices)
                (auth) Projects/Slices list of the user with <id>

            :return:
            """

        response = []
        current_user = self.get_current_user()

        # GET /users
        if not id and not o:
            cursor = yield r.table('users') \
                .pluck(self.fields['users']) \
                .merge(lambda user: {
                    'authority': r.table('authorities').get(user['authority']) \
                                                        .pluck(self.fields_short['authorities']) \
                                                        .default({'id' : user['authority']})
                }) \
                .run(self.dbconnection)
            while (yield cursor.fetch_next()):
                users = yield cursor.next()
                response.append(users)


        # GET /users/<id>
        elif not o and id and self.isUrn(id):
            if not current_user:
                self.userError('permission denied')
                return

            cursor = yield r.table('users') \
                .pluck(self.fields['users']) \
                .filter({'id': id}) \
                .merge(lambda user: {
                    'authority': r.table('authorities').get(user['authority']) \
                                                       .pluck(self.fields_short['authorities']) \
                                                       .default({'id': user['authority']})
                }) \
                .run(self.dbconnection)
            while (yield cursor.fetch_next()):
                user = yield cursor.next()
                response.append(user)

        # GET /users/[<id>/]projects
        elif o == 'projects':

            if not id or not self.isUrn(id):
                id = current_user['id']

            cursor = yield r.table(o) \
                .pluck(self.fields[o]) \
                .filter(lambda project: project["pi_users"].contains(id)) \
                .merge(lambda project: {
                    'authority': r.table('authorities').get(project['authority']) \
                           .pluck(self.fields_short['authorities']) \
                           .default({'id': project['authority']})
                }) \
                .run(self.dbconnection)
            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                response.append(item)

        # GET /users/[<id>/]slices
        elif o == 'slices':

            if not id or not self.isUrn(id):
                id = current_user['id']

            cursor = yield r.table(o) \
                .pluck(self.fields[o]) \
                .filter(lambda slice: slice["users"].contains(id)) \
                .merge(lambda slice: {
                    'project': r.table('projects').get(slice['project']) \
                           .pluck(self.fields_short['projects']) \
                           .default({'id': slice['project']})
                }) \
                .merge(lambda slice: {
                    'authority': r.table('authorities').get(slice['authority']) \
                           .pluck(self.fields_short['authorities']) \
                           .default({'id': slice['authority']})
                }) \
                .run(self.dbconnection)
            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                response.append(item)

        # GET /users/authorities
        elif not id and o == 'authorities':

            if not current_user:
                self.userError('permission denied')
                return

            cursor = yield r.table('authorities') \
                .pluck(self.fields['authorities']) \
                .filter(lambda authority:
                        authority["pi_users"].contains(current_user['id'])
                        or
                        authority["users"].contains(current_user['id'])) \
                .run(self.dbconnection)
            while (yield cursor.fetch_next()):
                authority = yield cursor.next()
                response.append(authority)


        else:
            self.userError("invalid request")
            return

        self.finish(json.dumps({"result": response}, cls=myJSONEncoder))



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
            self.userError("malformed request", e)
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
            self.userError("problem with request", e)
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
