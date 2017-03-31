import crypt
import json
import jwt
import logging
import re

from hmac import compare_digest as compare_hash
from email.utils import parseaddr

import rethinkdb as r
from myslice.db import dispatch, changes
from myslice.lib.util import myJSONEncoder
from myslice.db.activity import Event, EventAction, ObjectType, DataType
from myslice.db import dispatch
from myslice.web.rest import Api
from myslice.web.controllers.login import check_password, crypt_password

from tornado import gen, escape

logger = logging.getLogger('myslice.rest.users')

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

        if not check_password(password, user['password']):
            self.userError("password does not match")
            return

        # TODO: integrate OAuth2 and pass a token to the user
        self.set_current_user(user)

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

            - GET /users/<email>
                (auth) User with <email>

            - GET /users/(projects|slices|authorities)
                (auth) Projects/Slices/Authorities list of the authenticated user

            - GET /users/<id>/(projects|slices|authorities)
                (auth) Projects/Slices list of the user with <id>

            :return:
            """

        response = []
        current_user = self.get_current_user()
        if not current_user:
            self.userError("not authenticated")
            return

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


        # GET /users/<id> or /users/<email>
        elif not o and id:
            if self.isUrn(id):
                f = {'id':id}
            elif self.isEmail(id):
                f = {'email':id}
            if not current_user:
                self.userError('permission denied')
                return

            cursor = yield r.table('users') \
                .pluck(self.fields['users']) \
                .filter(f) \
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
                try:
                    id = current_user['id']
                except Exception as e:
                    self.serverError(" user is not logged in")
                    return


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
                try:
                    id = current_user['id']
                except Exception as e:
                    self.serverError(" user is not logged in")
                    return


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

        # GET /users/[<id>/]authorities
        elif o == 'authorities':
            if not id or not self.isUrn(id):
                try:
                    id = current_user['id']
                except Exception as e:
                    self.serverError(" user is not logged in")
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

        if data.get('authority', None) is None:
            self.userError("authority must be specified")
            return

        if data.get('first_name', None) is None:
            self.userError("first_name must be specified")
            return

        if data.get('last_name', None) is None:
            self.userError("last_name must be specified")
            return

        if data.get('email', None) is None:
            self.userError("email must be specified")
            return

        if not self.isEmail(data['email']):
            self.userError("Wrong Email address format")
            return

        user = None
        cursor = yield r.table('users') \
                .filter({'email':data['email']}) \
                .run(self.dbconnection)
        while (yield cursor.fetch_next()):
            user = yield cursor.next()
        if user:
            self.userError("This email is already registered")
            return

        if data.get('password', None) is None:
            self.userError("Password must be specified")
            return

        if len(data['password'])<8:
            self.userError("Password must be at least 8 characters")
            return

        # password must be encrypted before storing into DB
        data['password'] = crypt_password(data['password'])

        if data.get('terms', False) is False:
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
                'data': data,
                'notify': True,
            })
        except Exception as e:
            self.userError("Can't create request", e.message)
            return
        else:
            result = yield dispatch(self.dbconnection, event)
            self.write(json.dumps(
                {
                    "result": "success",
                    "events": result["generated_keys"],
                    "error": None,
                    "debug": None
                 }, cls=myJSONEncoder))

    @gen.coroutine
    def put(self, id=None, o=None):
        """
        PUT /users/<id>
        :return:
        """

        response = []
        current_user = self.get_current_user()

        if not current_user:
            self.userError('permission denied')
            return

        if not self.request.body:
            self.userError("empty request")
            return

        try:
            data = escape.json_decode(self.request.body)
        except json.decoder.JSONDecodeError as e:
            self.userError("malformed request", e.message)
            return

        # user id from DB
        user = None
        cursor = yield r.table('users') \
            .filter({'id': id}) \
            .run(self.dbconnection)
        while (yield cursor.fetch_next()):
            user = yield cursor.next()

        if not user:
            self.userError("this user %s does NOT exist" % id)
            return
        # If password changed, encrypt the new one
        if "password" in data and user["password"] != crypt_password(data["password"]):
            data["password"] = crypt_password(data["password"])

        # handle authority as dict
        if "authority" in data and type(data["authority"]) is dict:
            data["authority"] = data["authority"]["id"]

        # User's Slices are managed through the Projects Service
        # handle slices as dict
        if "slices" in data and type(data["slices"]) is dict:
            data["slices"] = data["slices"]["id"]

        # Update user's data
        try:
            event = Event({
                'action': EventAction.UPDATE,
                'user': current_user['id'],
                'object': {
                    'type': ObjectType.USER,
                    'id': id
                },
                'data': data
            })
        except Exception as e:
            self.userError("Can't create request", e.message)
            return
        else:
            result = yield dispatch(self.dbconnection, event)
            response = response + result["generated_keys"]

        # handle project as dict
        if all(isinstance(n, dict) for n in data['projects']):
            data['projects'] = [x['id'] for x in data['projects']]

        # Check the list of projects in data sent
        for p in data['projects']:
            # if the project is not in the list of the user's projects in the DB, user is a new pi
            if p not in user['projects']:
                # dispatch event add pi to project
                try:
                    event = Event({
                        'action': EventAction.ADD,
                        'user': current_user['id'],
                        'object': {
                            'type': ObjectType.PROJECT,
                            'id': p,
                        },
                        'data': {
                            'type' : DataType.PI,
                            'values' : [id]
                        }
                    })
                except AttributeError as e:
                    self.userError("Can't create request", e)
                    return
                except Exception as e:
                    self.userError("Can't create request", e)
                    return
                else:
                    result = yield dispatch(self.dbconnection, event)
                    response = response + result["generated_keys"]

        # Check user's projects in DB
        for p in user['projects']:
            # If the project is not in the data sent, remove the user from the project's pis
            if p not in data['projects']:
                # dispatch event add pi to project
                try:
                    event = Event({
                        'action': EventAction.REMOVE,
                        'user': current_user['id'],
                        'object': {
                            'type': ObjectType.PROJECT,
                            'id': p,
                        },
                        'data': {
                            'type' : DataType.PI,
                            'values' : [id]
                        }
                    })
                except AttributeError as e:
                    self.userError("Can't create request", e)
                    return
                except Exception as e:
                    self.userError("Can't create request", e)
                    return
                else:
                    result = yield dispatch(self.dbconnection, event)
                    response = response + result["generated_keys"]
        # handle authority as dict
        if all(isinstance(n, dict) for n in data['pi_authorities']):
            data['pi_authorities'] = [x['id'] for x in data['pi_authorities']]
        # Check the list of pi_authorities in data sent
        for a in data['pi_authorities']:
            # if the authority is not in the list of the user's pi_authorities in the DB, user is a new pi
            # XXX pi_authorities contains also projects, to be changed in myslicelib
            if a not in user['pi_authorities'] and len(a.split('+')[1].split(':'))<3:
                # dispatch event add pi to authority
                try:
                    event = Event({
                        'action': EventAction.ADD,
                        'user': current_user['id'],
                        'object': {
                            'type': ObjectType.AUTHORITY,
                            'id': a,
                        },
                        'data': {
                            'type' : DataType.PI,
                            'values' : [id]
                        }
                    })
                except AttributeError as e:
                    self.userError("Can't create request", e)
                    return
                except Exception as e:
                    self.userError("Can't create request", e)
                    return
                else:
                    result = yield dispatch(self.dbconnection, event)
                    response = response + result["generated_keys"]

        # Check user's pi_authorities in DB
        for a in user['pi_authorities']:
            # If the authority is not in the data sent, remove the user from the authority pis
            # XXX pi_authorities contains also projects, to be changed in myslicelib
            if a not in data['pi_authorities'] and len(a.split('+')[1].split(':'))<3:
                # dispatch event add pi to project
                try:
                    event = Event({
                        'action': EventAction.REMOVE,
                        'user': current_user['id'],
                        'object': {
                            'type': ObjectType.AUTHORITY,
                            'id': a,
                        },
                        'data': {
                            'type' : DataType.PI,
                            'values' : [id]
                        }
                    })
                except AttributeError as e:
                    self.userError("Can't create request", e)
                    return
                except Exception as e:
                    self.userError("Can't create request", e)
                    return
                else:
                    result = yield dispatch(self.dbconnection, event)
                    response = response + result["generated_keys"]

        self.write(json.dumps(
            {
                "result": "success",
                "events": response,
                "error": None,
                "debug": None
             }, cls=myJSONEncoder))

    @gen.coroutine
    def delete(self, id, o=None):
        """
        DELETE /users/<id>
        :return:
        """
        # A user has the right to delete his own account
        # Check if the current user is PI of the authority of the user 
        # Or an upper authority 
        current_user = self.get_current_user()
        if not current_user:
            self.userError("not authenticated")
            return
        try:
            # user id from DB
            user = None
            cursor = yield r.table('users') \
                .filter({'id': id}) \
                .run(self.dbconnection)
            while (yield cursor.fetch_next()):
                user = yield cursor.next()

            if not user:
                self.userError("this user %s does NOT exist" % id)
                return

            if current_user['id']!=id:
                # Check if the user isAdmin 
                admin = self.isAdmin()
                a = yield r.table('authorities').get(user['authority']).run(self.dbconnection)
                if current_user['id'] not in a['pi_users'] and not admin: 
                    self.userError("your user has no rights on authority: %s" % id)
                    return
        except Exception as e:
            self.userError(e)
            return
        try:
            event = Event({
                'action': EventAction.DELETE,
                'user': current_user['id'],
                'object': {
                    'type': ObjectType.USER,
                    'id': id,
                },
                'data': {'authority': user['authority']}
            })
        except AttributeError as e:
            self.userError("Can't create request", e)
            return
        except Exception as e:
            self.userError("Can't create request", e)
            return
        else:
            result = yield dispatch(self.dbconnection, event)
            self.write(json.dumps(
                {
                    "result": "success",
                    "events": result["generated_keys"],
                    "error": None,
                    "debug": None
                 }, cls=myJSONEncoder))

class ProfileHandler(Api):


    @gen.coroutine
    def get(self):
        """
        GET /profile

        Logged in User Profile

        :return:
        """
        # TODO: id must be a valid URN
        try:
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
        except Exception:
            self.userError("not authenticated ")
            return
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
                    return

class UserTokenHandler(Api):

    @gen.coroutine
    def get(self):
        """
        GET /usertoken

        :return:
        """
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
                                "projects" : user['projects'],
                                "slices" : user['slices'],
                                },
                                secret, algorithm='HS256')
        except Exception as e:
            self.serverError("token encryption failed", e)
            return
        self.finish(token)

    @gen.coroutine
    def post(self):
        """
        POST /usertoken

        :return:
        user
        """
        secret = self.application.settings['token_secret'] # used in websockets
        encrypted_string = self.request.body
        try:
            user = jwt.decode(encrypted_string, secret, algorithms=['HS256'])
        except Exception as e:
            logger.error('Token Decrption error %s' % e)
            self.userError('Token Decrption error')
            return

        self.finish(json.dumps(user, cls=myJSONEncoder))
