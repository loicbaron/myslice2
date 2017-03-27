import json
import re

from pprint import pprint

import rethinkdb as r

from myslice.lib.util import myJSONEncoder
from myslice.web.rest import Api

from myslice.db.activity import Event, EventAction, ObjectType, DataType
from myslice.db import dispatch

from myslice.web.controllers.login import crypt_password
from tornado import gen, escape

class AuthoritiesHandler(Api):

    @gen.coroutine
    def get(self, id=None, o=None):
        """
            - GET /authorities
                (public) Authorities list

            - GET /authorities/<id>
                (public) Authority with <id>

            - GET /authorities/(users|projects)
                (auth) Users/Projects list of the authority of the
                logged in user

            - GET /authorities/<id>/(users|projects)
                (auth) Users/Projects list of the authority with <id>

            :return:
            """
            
        response = []
        current_user = self.get_current_user()

        # GET /authorities
        if not id and not o:
            cursor = yield r.table('authorities') \
                            .pluck(self.fields['authorities']) \
                            .run(self.dbconnection)
            while (yield cursor.fetch_next()):
                authority = yield cursor.next()
                if authority['name'] is None:
                    authority['name'] = authority['shortname'].title()
                response.append(authority)


        # GET /authorities/<id>
        elif not o and id and self.isUrn(id):
            if not current_user:
                self.userError('permission denied')
                return

            try:
                # Check if the user has the right to GET an authority, PI of an upper authority
                a = yield r.table('authorities').get(id).run(self.dbconnection)
                if not a:
                    self.userError("this authority %s does not exist" % id)
                    return
                root_auth = yield r.table('authorities').get(a['authority']).run(self.dbconnection)
                if self.current_user['id'] not in a['pi_users'] and self.current_user['id'] not in root_auth['pi_users']:
                    self.userError("your user has no rights on authority: %s" % id)
                    return
            except Exception:
                import traceback
                traceback.print_exc()
                self.userError("not authenticated")
                return

            cursor = yield r.table('authorities') \
                            .pluck(self.fields['authorities']) \
                            .filter({'id': id}) \
                            .run(self.dbconnection)
            while (yield cursor.fetch_next()):
                authority = yield cursor.next()
                if authority['name'] is None:
                    authority['name'] = authority['shortname'].title()
                response.append(authority)

        # GET /authorities/(users|projects)
        elif not id and o in ['users', 'projects']:
            if not current_user:
                self.userError('permission denied')
                return

            cursor = yield r.table(o) \
                            .pluck(self.fields[o]) \
                            .filter({"authority": current_user['authority']}) \
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
                item = yield cursor.next()
                if 'name' in item and item['name'] is None:
                    item['name'] = item['shortname'].title()
                response.append(item)

        # GET /authorities/<id>/(users|projects)
        elif id and self.isUrn(id) and o in ['users', 'projects']:
            try:
                # Check if the user has the right to GET an authority, PI of an upper authority
                a = yield r.table('authorities').get(id).run(self.dbconnection)
                if not a:
                    self.userError("this authority %s does not exist" % id)
                    return
                root_auth = yield r.table('authorities').get(a['authority']).run(self.dbconnection)
                if self.current_user['id'] not in a['pi_users'] and self.current_user['id'] not in root_auth['pi_users']:
                    self.userError("your user has no rights on authority: %s" % id)
                    return
            except Exception:
                import traceback
                traceback.print_exc()
                self.userError("not authenticated")
                return

            if o=='users':
                cursor = yield r.table(o) \
                            .pluck(self.fields[o]) \
                            .filter({"authority": id}) \
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
            else:
                cursor = yield r.table(o) \
                            .pluck(self.fields[o]) \
                            .filter({"authority": id}) \
                            .run(self.dbconnection)
            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                if 'name' in item and item['name'] is None:
                    item['name'] = item['shortname'].title()
                response.append(item)

        else:
            self.userError("invalid request {} {}".format(id, o))
            return

        self.finish(json.dumps({"result": response}, cls=myJSONEncoder))

    @gen.coroutine
    def post(self):
        """
        POST /authorities
        { 'name': 'Test Authority', 'shortname': 'test_authority' }
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

        if data.get('name', None) is None:
            self.userError("Authority name must be specified")
            return

        if data.get('shortname', None) is None:
            self.userError("Authority shortname must be specified")
            return

        # if new users are specified to be added to the authority
        if len(data.get('users', [])) > 0:
            for u in data['users']:
                if not isinstance(u, dict):
                    self.userError("New user properties under a new authority must be sent as dict")
                    return
                if u.get('first_name', None) is None:
                    self.userError("User first_name must be specified")
                    return
                if u.get('last_name', None) is None:
                    self.userError("User last_name must be specified")
                    return
                if u.get('password', None) is None:
                    self.userError("User password must be specified")
                    return
                if len(u['password'])<8:
                    self.userError("Password must be at least 8 characters")
                    return
                # password must be encrypted before storing into DB
                u['password'] = crypt_password(u['password'])
                if u.get('email', None) is None:
                    self.userError("User email must be specified")
                    return
                if not self.isEmail(u['email']):
                    self.userError("Wrong Email address")
                    return
                if u.get('terms', False) is False:
                    self.userError("User must accept terms and conditions")
                    return

        # if pi_users are specified to manage the authority
        if len(data.get('pi_users', [])) > 0:
            for u in data['pi_users']:
                # if pi_user is a New User we need at least his/her email
                if isinstance(u, dict):
                    if u.get('email', None) is None:
                        self.userError("email of a new pi_user must be specified")
                        return
                    if not self.isEmail(u['email']):
                        self.userError("Wrong Email address")
                        return
                    if not any([user['email'] == u['email'] for user in data['users']]):
                        self.userError("email %s of pi_user is not among new users" % u['email'])
                        return

        if not self.get_current_user():
            # authority registration for new user
            current_user_id = None
        else:
            # admin create user directly
            current_user_id = self.get_current_user()['id']

        try:
            event = Event({
                'action': EventAction.CREATE,
                'user': current_user_id,
                'object': {
                    'type': ObjectType.AUTHORITY,
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
                    "events": result["generated_keys"],
                    "error": None,
                    "debug": None
                 }, cls=myJSONEncoder))


    @gen.coroutine
    def put(self, id=None, o=None):
        """
        PUT /authorities/<id>
        { authority object }
        :return:
        """
        try:
            # Check if the user has the right to Update an authority, PI of an upper authority
            a = yield r.table('authorities').get(id).run(self.dbconnection)
            if not a:
                self.userError("this authority %s does not exist" % id)
                return
            root_auth = yield r.table('authorities').get(a['authority']).run(self.dbconnection)
            # TBD: admin or pi?
            #if self.current_user['id'] not in a['pi_users'] and self.current_user['id'] not in root_auth['pi_users']:
            # only root_auth admin at the moment
            if self.current_user['id'] not in root_auth['pi_users']:
                self.userError("your user has no rights on authority: %s" % id)
                return
        except Exception:
            self.userError("not authenticated ")
            return

        events = []
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

        # authority id from DB
        cursor = yield r.table('authorities') \
            .filter({'id': id}) \
            .run(self.dbconnection)
        while (yield cursor.fetch_next()):
            authority = yield cursor.next()

        # handle authority as dict
        if "authority" in data and type(data["authority"]) is dict:
            data["authority"] = data["authority"]["id"]

        # Slices should be under a project (Legacy slices under an authority) 
        # handle slices as dict
        if "slices" in data and type(data["slices"]) is dict:
            data["slices"] = data["slices"]["id"]

        # Users belong to an Authority, it can NOT be changed
        # handled by POST /users & DELETE /users/<id>
        if "users" in data and type(data["users"]) is dict:
            data["users"] = data["users"]["id"]

        # Update authority data
        try:
            event = Event({
                'action': EventAction.UPDATE,
                'user': current_user['id'],
                'object': {
                    'type': ObjectType.AUTHORITY,
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

        # handle pi_user as dict
        if all(isinstance(n, dict) for n in data['pi_users']):
            data['pi_users'] = [x['id'] for x in data['pi_users']]

        e = self.update_authority(data, authority)
        if e:
            events.append(e)

        # adding pi users
        events += self.add_pi_users(data, authority, ObjectType.AUTHORITY)

        # removing pi users
        events += self.remove_pi_users(data, authority, ObjectType.AUTHORITY)

        for e in events:
            result = yield dispatch(self.dbconnection, e)
            response = response + result['generated_keys']

        ##
        # projects
        # This is handled by the POST /projects and DELETE /projects/<id> calls

        ##
        # users
        # This is handled by the POST /users and DELETE /users/<id> calls

        self.write(json.dumps(
            {
                "result": "success",
                "events": response,
                "error": None,
                "debug": None
             }, cls=myJSONEncoder))

    def update_authority(self, data, project):
        # update authority data only if it has changed
        # TODO: check what we can change
        return False
        # Update project properties
        # try:
        #     event = Event({
        #         'action': EventAction.UPDATE,
        #         'user': current_user['id'],
        #         'object': {
        #             'type': ObjectType.PROJECT,
        #             'id': project['id']
        #         },
        #         'data': data
        #     })
        # except Exception as e:
        #     self.userError("Can't create request", e.message)
        #     return
        # else:
        #     result = yield dispatch(self.dbconnection, event)
        #     response = response + result["generated_keys"]

    @gen.coroutine
    def delete(self, id, o=None):
        """
                DELETE /authorities/<id>
                :return:
        """
        try:
            # Check if the user has the right to delete an authority, PI of an upper authority
            a = yield r.table('authorities').get(id).run(self.dbconnection)
            if not a:
                self.userError("this authority %s does not exist" % id)
                return
            root_auth = yield r.table('authorities').get(a['authority']).run(self.dbconnection)
            if self.current_user['id'] not in a['pi_users'] and self.current_user['id'] not in root_auth['pi_users']:
                self.userError("your user has no rights on authority: %s" % id)
                return
        except Exception:
            import traceback
            traceback.print_exc()
            self.userError("not authenticated")
            return
        try:
            event = Event({
                'action': EventAction.DELETE,
                'user': self.current_user['id'],
                'object': {
                    'type': ObjectType.AUTHORITY,
                    'id': id,
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
            self.write(json.dumps(
                {
                    "result": "success",
                    "events": result["generated_keys"],
                    "error": None,
                    "debug": None
                 }, cls=myJSONEncoder))
