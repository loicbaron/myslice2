import json

from pprint import pprint

import rethinkdb as r

from myslice.lib.util import myJSONEncoder
from myslice.web.rest import Api

from myslice.db.activity import Event, EventAction, ObjectType
from myslice.db import dispatch
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

            cursor = yield r.table('authorities') \
                            .pluck(self.fields['authorities']) \
                            .filter({'id': id}) \
                            .filter(lambda authority:
                                           authority["pi_users"].contains(current_user['id'])
                                           or
                                           authority["users"].contains(current_user['id'])) \
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

        if not data['name']:
            self.userError("Authority name must be specified")
            return

        if not data['shortname']:
            self.userError("Authority shortname must be specified")
            return

        try:
            event = Event({
                'action': EventAction.CREATE,
                'user': self.get_current_user()['id'],
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
            root_auth = yield r.table('authorities').get(a.authority).run(self.dbconnection)
            # TBD: admin or pi?
            #if self.current_user['id'] not in a['pi_users'] and self.current_user['id'] not in root_auth['pi_users']:
            # only root_auth admin at the moment
            if self.current_user['id'] not in root_auth['pi_users']:
                self.userError("your user has no rights on authority: %s" % id)
                return
        except Exception:
            self.userError("not authenticated ")
            return

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
        ##
        # pi_users
        # authority ADD pis
        for auth_pi in data['pi_users']:
            # new pi
            if auth_pi not in authority['pi_users']:
                # dispatch event add pi to project
                try:
                    event = Event({
                        'action': EventAction.ADD,
                        'user': current_user['id'],
                        'object': {
                            'type': ObjectType.AUTHORITY,
                            'id': id,
                        },
                        'data': {
                            'type' : DataType.PI,
                            'values' : auth_pi
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

        ##
        # authority REMOVE pis
        for auth_pi in authority['pi_users']:
            if auth_pi not in data['pi_users']:
                # dispatch event remove pi from authority
                try:
                    event = Event({
                        'action': EventAction.REMOVE,
                        'user': self.current_user['id'],
                        'object': {
                            'type': ObjectType.AUTHORITY,
                            'id': id,
                        },
                        'data': {
                            'type': DataType.PI,
                            'values': auth_pi
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

    @gen.coroutine
    def delete(self, id, o=None):
        """
                DELETE /authorities/<id>
                :return:
        """
        try:
            # Check if the user has the right to delete an authority, PI of an upper authority
            a = yield r.table('authorities').get(id).run(self.dbconnection)
            root_auth = yield r.table('authorities').get(a.authority).run(self.dbconnection)
            if self.current_user['id'] not in a['pi_users'] and self.current_user['id'] not in root_auth['pi_users']:
                self.userError("your user has no rights on authority: %s" % id)
                return
        except Exception:
            self.userError("not authenticated ")
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
