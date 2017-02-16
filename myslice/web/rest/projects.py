import json

import rethinkdb as r

from myslice.lib.util import myJSONEncoder
from myslice.web.rest import Api

from myslice.db.activity import Event, EventAction, ObjectType, DataType
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
            if not current_user:
                self.userError('permission denied')
                return
            cursor = yield r.table('projects') \
                .pluck(self.fields['projects']) \
                .filter(lambda project: project["pi_users"].contains(current_user['id'])) \
                .merge(lambda project: {
                    'authority': r.table('authorities').get(project['authority']) \
                                                        .pluck(self.fields_short['authorities']) \
                                                        .default({'id': project['authority']})
                }) \
                .merge(lambda project: {
                    'slices': r.table('slices') \
                       .get_all(r.args(project['slices'])) \
                       .pluck(self.fields_short['slices']) \
                       .coerce_to('array')
                }) \
                .merge(lambda project: {
                    'pi_users': r.table('users') \
                           .get_all(r.args(project['pi_users'])) \
                           .pluck(self.fields_short['users']) \
                           .coerce_to('array')
                }) \
                .merge(lambda project: {
                    'users': r.table('users') \
                           .get_all(r.args(project['users'])) \
                           .pluck(self.fields_short['users']) \
                           .coerce_to('array')
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

        if data.get('authority', None) is None:
            self.userError("authority must be specified")
            return

        if data.get('name', None) is None:
            self.userError("Project name must be specified")
            return

        if data.get('description', None) is None:
            self.userError("Project description must be specified")
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
                    "events": result["generated_keys"],
                    "error": None,
                    "debug": None
                 }, cls=myJSONEncoder))

    @gen.coroutine
    def put(self, id=None, o=None):
        """
        PUT /projects/<id>
        { project object }
        :return:
        """

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

        # project id from DB
        cursor = yield r.table('projects') \
            .pluck(self.fields['projects']) \
            .filter({'id': id}) \
            .filter(lambda project:
                    project["pi_users"].contains(current_user['id']) or
                    project["users"].contains(current_user['id'])) \
            .run(self.dbconnection)
        while (yield cursor.fetch_next()):
            project = yield cursor.next()

        if not project:
            self.userError("project not found, problem with db")
            return

        # handle authority as dict
        if "authority" in data and type(data["authority"]) is dict:
            data["authority"] = data["authority"]["id"]

        # handle slices as dict
        if all(isinstance(n, dict) for n in data['slices']):
            data['slices'] = [x['id'] for x in data['slices']]

        # handle pi_user as dict
        if all(isinstance(n, dict) for n in data['pi_users']):
            data['pi_users'] = [x['id'] for x in data['pi_users']]

        e = self.update_project(data, project)
        if e:
            events.append(e)

        # adding pi users
        events += self.add_pi_users(data, project, ObjectType.PROJECT)

        # removing pi users
        events += self.remove_pi_users(data, project, ObjectType.PROJECT)

        for e in events:
            result = yield dispatch(self.dbconnection, e)
            response = response + result['generated_keys']

        ##
        # slices
        # This is handled by the POST /slices and DELETE /slices/<id> calls

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
        DELETE /projects/<id>
        :return:
        """
        # Check if the user is PI of the Project
        try:
            p = yield r.table('projects').get(id).run(self.dbconnection)
            u = yield r.table('users').get(self.current_user['id']).run(self.dbconnection)
            if not self.current_user['id'] in p['pi_users'] and p['authority'] not in u['pi_authorities']:
                self.userError("your user has no rights on project: %s" % id)
                return
        except Exception:
            self.userError("not authenticated or project not specified")
            return

        try:
            event = Event({
                'action': EventAction.DELETE,
                'user': self.current_user['id'],
                'object': {
                    'type': ObjectType.PROJECT,
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

    def update_project(self, data, project):
        # update project data only if it has changed
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


