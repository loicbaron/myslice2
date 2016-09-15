import crypt
import json
import jwt
import re

from hmac import compare_digest as compare_hash
from email.utils import parseaddr

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
        #         'user': self.get_current_user()['id'],
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
                .merge(lambda user: {
                'pi_authorities': r.table('authorities').get_all(r.args(user['pi_authorities'])) \
                                                       .pluck(self.fields_short['authorities']) \
                                                       .coerce_to('array')
                 }) \
                .merge(lambda user: {
                    'projects': r.table('projects') \
                           .get_all(r.args(user['projects'])) \
                           .pluck(self.fields_short['projects']) \
                           .coerce_to('array')
                }) \
                .merge(lambda user: {
                    'slices': r.table('slices') \
                           .get_all(r.args(user['slices'])) \
                           .pluck(self.fields_short['slices']) \
                           .coerce_to('array')
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
                .merge(lambda user: {
                'pi_authorities': r.table('authorities').get_all(r.args(user['pi_authorities'])) \
                                                       .pluck(self.fields_short['authorities']) \
                                                       .coerce_to('array')
                 }) \
                .merge(lambda user: {
                    'projects': r.table('projects') \
                           .get_all(r.args(user['projects'])) \
                           .pluck(self.fields_short['projects']) \
                           .coerce_to('array')
                }) \
                .merge(lambda user: {
                    'slices': r.table('slices') \
                           .get_all(r.args(user['slices'])) \
                           .pluck(self.fields_short['slices']) \
                           .coerce_to('array')
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
    def post(self):
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
            self.userError("Authority must be specified")
            return

        if not data['first_name']:
            self.userError("Firstname must be specified")
            return
        if not data['last_name']:
            self.userError("Lastname must be specified")
            return

        if not data['email']:
            self.userError("Email must be specified")
            return

        pattern = "^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"
        if not re.match(pattern, data['email']):
            self.userError("Wrong Email address")
            return

        if not data['password']:
            self.userError("Password must be specified")
            return

        if len(data['password'])<8:
            self.userError("Password must be at least 8 characters")
            return

        if not data['terms']:
            self.userError("Please read and accept the terms and conditions.")
            return

        if not self.get_current_user():
            # usr registration
            current_user_id = None
        else:
            # admin create user directly
            current_user_id = self.get_current_user()['id']

        try:
            event = Event({
                'action': EventAction.CREATE,
                'user': current_user_id,
                'object': {
                    'type': ObjectType.USER,
                    'id': None
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
        # Check if the current user is PI of the authority of the user 
        # Or an upper authority 
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

        profile = yield r.table('users')\
                .get(self.get_current_user()['id']) \
                .pluck(self.fields['profile']) \
                .merge(lambda user: {
                'authority': r.table('authorities').get(user['authority']) \
                                                       .pluck(self.fields_short['authorities']) \
                                                       .default({'id': user['authority']})
                 }) \
                .merge(lambda user: {
                'pi_authorities': r.table('authorities').get_all(r.args(user['pi_authorities'])) \
                                                       .pluck(self.fields_short['authorities']) \
                                                       .coerce_to('array')
                 }) \
                .merge(lambda user: {
                    'projects': r.table('projects') \
                           .get_all(r.args(user['projects'])) \
                           .pluck(self.fields_short['projects']) \
                           .coerce_to('array')
                }) \
                .merge(lambda user: {
                    'slices': r.table('slices') \
                           .get_all(r.args(user['slices'])) \
                           .pluck(self.fields_short['slices']) \
                           .coerce_to('array')
                }) \
                .run(self.dbconnection)

        self.write(json.dumps({"result": profile}, cls=myJSONEncoder))

    @gen.coroutine
    def put(self):
        """
        PUT /profile

        :return:
        """
        try:
            data = escape.json_decode(self.request.body)
        except json.decoder.JSONDecodeError as e:
            self.userError("malformed request", e)
            return
        except Exception as e:
            self.userError("malformed request", e)
            return

        # filter fields
        try:
            for key in data:
                if key not in ['first_name', 'last_name', 'bio', 'url', 'generate_keys']:
                    raise KeyError
        except Exception as e:
            self.userError("malformed request", e)
            return


        user_id = self.get_current_user()['id']

        try:
            event = Event({
                'action': EventAction.UPDATE,
                'user': user_id ,
                'object': {
                    'type': ObjectType.USER,
                    'id': user_id ,
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

                    feed = yield r.table('users') \
                        .pluck(self.fields['profile']) \
                        .filter({'id': user_id}) \
                        .merge(lambda user: {
                        'authority': r.table('authorities').get(user['authority']) \
                                                       .pluck(self.fields_short['authorities']) \
                                                       .default({'id': user['authority']})
                        }) \
                        .run(self.dbconnection)

                    yield feed.fetch_next()
                    profile = yield feed.next()
                    self.finish(json.dumps({"result": profile}, cls=myJSONEncoder))
                
                else:
                    self.userError("updated failed", result['new_val'])

class UserTokenHandler(Api):
    """
    PUT /usertoken

    :return:
    """

    @gen.coroutine
    def get(self):

        admin = self.isAdmin()

        try:
            current_user_id = self.get_current_user()['id']
        except Exception as e:
            self.serverError("unidentified user")
            return
       
        pi_auth = [] 
        
        # if not admin
        if not admin:
            user = yield r.table('users').get(current_user_id).run(self.dbconnection)
            pi_auth = user['pi_authorities']

        try:
            secret = self.application.settings['token_secret'] # used in websockets
            token = jwt.encode({
                                "id" : current_user_id,
                                "admin" : admin,
                                "pi_auth" : pi_auth,
                                },
                                secret, algorithm='HS256')
        except Exception as e:
            self.serverError("token encryption failed", e)
            return
        
        self.finish(token)


