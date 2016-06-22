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
        GET /projects/[<id>[/(users|slices)]]

        Project list or project with <id>
        User or Slice list part of project with <id>

        :return:
        """

        project = None
        response = []

        if id:
            # get the project
            cursor = yield r.table('projects') \
                .pluck(self.fields['projects']) \
                .filter(lambda project:
                        project["id"].contains(id) and
                        project["pi_users"].contains(self.get_current_user_id())
                ) \
                .merge(lambda project: {
                    'authority': r.table('authorities').get(project['authority']).pluck(self.fields_short['authorities'])
                }) \
                .run(self.dbconnection)

            while (yield cursor.fetch_next()):
                project = yield cursor.next()

            if not project:
                self.userError("no project found or permission denied")
                return

            # GET /projects/<id>/users
            if o == 'users':
                # users in a project
                cursor = yield r.table('users') \
                                .pluck(self.fields['users']) \
                                .filter(lambda user:
                                    user["projects"].contains(id)
                                ) \
                                .merge(lambda project: {
                                    'authority': r.table('authorities').get(project['authority']).pluck(
                                        self.fields_short['authorities'])
                                }) \
                                .run(self.dbconnection)

                while (yield cursor.fetch_next()):
                    item = yield cursor.next()
                    response.append(item)

            # GET /projects/<id>/slices
            elif o == 'slices':
                # users in a project
                cursor = yield r.table('slices') \
                                .pluck(self.fields['slices']) \
                                .filter({"project": id}) \
                                .merge(lambda slice: {
                                    'project': r.table('projects').get(slice['project']).pluck(
                                    self.fields_short['projects'])
                                }) \
                                .merge(lambda slice: {
                                    'authority': r.table('authorities').get(slice['project']['authority']).pluck(
                                        self.fields_short['authorities'])
                                }) \
                                .run(self.dbconnection)



                while (yield cursor.fetch_next()):
                    item = yield cursor.next()
                    response.append(item)

            # GET /projects/<id>
            elif o is None:
                response.append(project)

            else:
                self.userError("invalid request")
                return

        # GET /projects
        else:
            # list of projects of a user
            cursor = yield r.table('projects') \
                            .pluck(self.fields['projects']) \
                            .filter(lambda project: project["pi_users"].contains(self.get_current_user_id()))\
                            .merge(lambda project: {
                                'authority': r.table('authorities').get(project['authority']).pluck(self.fields_short['authorities'])
                            }).run(self.dbconnection)

            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                response.append(item)

        self.write(json.dumps({"result": response}, cls=myJSONEncoder))

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
            if not 'authority' in data:
                self.userError("missing required parameter authority")
                return

            event = Event({
                'action': EventAction.CREATE,
                'user': self.get_current_user_id(), 
                'object': {
                    'type': ObjectType.PROJECT,
                    'id': None,
                },
                'data': data
            })
        except AttributeError as e:
            self.userError("Can't create request", str(e))
            return
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
        PUT /projects/<id>
        :return:
        """
        pass

    @gen.coroutine
    def delete(self):
        """
        DELETE /projects/<id>
        :return:
        """
        pass
