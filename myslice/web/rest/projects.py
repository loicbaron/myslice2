import json

import rethinkdb as r

from myslice.lib.util import myJSONEncoder
from myslice.web.rest import Api

from myslice.db.activity import Event, EventAction, ObjectType
from myslice.db import dispatch

from tornado import gen, escape

class ProjectsHandler(Api):

    @gen.coroutine
    def get(self, id):
        """
        GET /projects/[<id>]

        Project list or project with <id>

        :return:
        """

        projects = []
        print(self.request.arguments)

        # TODO: id must be a valid URN
        if id:
            result = yield r.table('projects').get(id).run(self.dbconnection)
            projects.append(result)
        else:
            # USER
            # public projects
            # protected projects where user is memberi/PI of the authority
            # projects where user is PI (including private)
            user = yield r.table('users').get(self.get_current_user_id()).run(self.dbconnection)
            for p in user['projects']:
                result = yield r.table('projects').get(p).run(self.dbconnection)
                projects.append(result)

            # XXX ADMIN = NO FILTER
            #cursor = yield r.table('projects').run(self.dbconnection)

            #while (yield cursor.fetch_next()):
            #    result = yield cursor.next()
            #    projects.append(result)

        self.write(json.dumps({"result": projects}, cls=myJSONEncoder))

    @gen.coroutine
    def post(self, params):
        """
        POST /projects
        { data: { name: string, label: string, description: string } }
        :return:
        """
        print(params)
        print(self.request.body)
        try:
            data = escape.json_decode(self.request.body)['data']
        except json.decoder.JSONDecodeError as e:
            self.userError("malformed request", e.message)
            return

        try:
            event = Event({
                'action': EventAction.CREATE,
                'user': 'user_id_todo_from_auth',
                'object': {
                    'type': ObjectType.PROJECT,
                    'id': 'generated id from data name'
                },
                'data': data
            })
        except Exception as e:
            self.userError("problem with request", e.message)
            return
        else:
            result = yield dispatch(self.dbconnection, event)
            # data = self.get_argument('event','no data')
            self.write(json.dumps({"result": "ok"}, cls=myJSONEncoder))
            print(event)

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
