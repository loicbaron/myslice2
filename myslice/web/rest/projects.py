import json

import rethinkdb as r

from myslice.lib.util import myJSONEncoder
from myslice.web.rest import Api

from myslice.db.activity import Event, EventAction, ObjectType
from myslice.db import dispatch

from tornado import gen, escape

class ProjectsHandler(Api):

    @gen.coroutine
    def get(self, id=None, o=None):
        """
            - GET /projects
                (public) Projects list

            - GET /projects/<id>
                (public) Project with <id>

            - GET /projects/<id>/(users|slices)
                (auth) Users/Slices list of the project with <id>

            :return:
            """

        response = []
        current_user = self.get_current_user()

        # GET /projects
        if not id and not o:
            cursor = yield r.table('projects') \
                .pluck(self.fields['projects']) \
                .filter(lambda project: project["pi_users"].contains(current_user['id'])) \
                .merge(lambda project: {
                    'authority': r.table('authorities').get(project['authority']) \
                                                        .pluck(self.fields_short['authorities']) \
                                                        .default({'id': project['authority']})
                    }) \
                .run(self.dbconnection)
            while (yield cursor.fetch_next()):
                project = yield cursor.next()
                response.append(project)


        # GET /projects/<id>
        elif not o and id and self.isUrn(id):
            if not current_user:
                self.userError('permission denied')
                return

            cursor = yield r.table('projects') \
                .pluck(self.fields['projects']) \
                .filter({'id': id}) \
                .filter(lambda project:
                        project["pi_users"].contains(current_user['id']) or
                        project["users"].contains(current_user['id'])) \
                .merge(lambda project: {
                    'authority': r.table('authorities').get(project['authority']) \
                                                        .pluck(self.fields_short['authorities']) \
                                                        .default({'id': project['authority']})
                }) \
                .run(self.dbconnection)
            while (yield cursor.fetch_next()):
                project = yield cursor.next()
                response.append(project)

        # GET /projects/<id>/users
        elif id and self.isUrn(id) and o == 'users':
            cursor = yield r.table(o) \
                .pluck(self.fields[o]) \
                .filter(lambda user: user["projects"].contains(id)) \
                .merge(lambda user: {
                    'authority': r.table('authorities').get(user['authority']) \
                                                        .pluck(self.fields_short['authorities']) \
                                                        .default({'id': user['authority']})
                }) \
                .run(self.dbconnection)
            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                response.append(item)

        # GET /projects/<id>/slices
        elif id and self.isUrn(id) and o == 'slices':
            cursor = yield r.table(o) \
                .pluck(self.fields[o]) \
                .filter({ "project": id }) \
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

        else:
            self.userError("invalid request")
            return

        self.finish(json.dumps({"result": response}, cls=myJSONEncoder))


    @gen.coroutine
    def post(self, id=None, o=None):
        """
        POST /projects
        { name: string, label: string, description: string }
        :return:
        """

        if not self.request.body:
            self.userError("empty request")
            return

        try:
            data = escape.json_decode(self.request.body)
        except json.decoder.JSONDecodeError as e:
            self.userError("malformed request", e.message)
            return

        try:
            data['authority'] = self.current_user['authority']
        except Exception:
            self.userError("not authenticated")
            return

        try:
            event = Event({
                'action': EventAction.CREATE,
                'user': self.current_user['id'],
                'object': {
                    'type': ObjectType.PROJECT,
                    'id': None,
                },
                'data': data
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
                    "error": None,
                    "debug": None
                }, cls=myJSONEncoder))

    @gen.coroutine
    def put(self, id=None, o=None):
        """
        PUT /projects/<id>
        { 'action':'add|remove', ‘users’ : [ <id user>, <id user>, … ] }
        :return:
        """
        if not self.request.body:
            self.userError("empty request")
            return

        try:
            data = escape.json_decode(self.request.body)
        except json.decoder.JSONDecodeError as e:
            self.userError("malformed request", e.message)
            return

        if 'users' in data:
            data['type'] = "USER"
            data['values'] = data['users']
            del data['users']
        else:
            self.userError("ObjectType not supported")

        try:
            if data['action'].lower() == 'add':
                action = EventAction.ADD
            elif data['action'].lower() == 'remove':
                action = EventAction.REMOVE
            else:
                raise ValueError("action %s not supported" % data['action'])
        except Exception as e:
            self.userError("malformed request", e)

        try:
            event = Event({
                'action': action,
                'user': self.current_user['id'],
                'object': {
                    'type': ObjectType.PROJECT,
                    'id': id,
                },
                'data': data
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
                    "error": None,
                    "debug": None
                }, cls=myJSONEncoder))

    @gen.coroutine
    def delete(self):
        """
        DELETE /projects/<id>
        :return:
        """
        # Check if the user is PI of the Project
        pass
