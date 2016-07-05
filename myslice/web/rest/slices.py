import json

import rethinkdb as r

from myslice.lib.util import myJSONEncoder
from myslice.web.rest import Api

from myslice.db.activity import Event, EventAction, ObjectType
from myslice.db import dispatch

from tornado import gen, escape

class SlicesHandler(Api):

    @gen.coroutine
    def get(self, id=None, o=None):
        """
            - GET /slices
                (public) Slices list

            - GET /slices/<id|hrn>
                (public) Slices with <id|hrn>

            - GET /slices/<id|hrn>/(users|resources)
                (auth) Users/Resources list of the slice with <id|hrn>

            :return:
            """

        response = []
        current_user = self.get_current_user()

        # GET /slices
        if not id and not o:
            cursor = yield r.table('slices') \
                .pluck(self.fields['slices']) \
                .merge(lambda slice: {
                    'authority': r.table('authorities').get(slice['authority']) \
                           .pluck(self.fields_short['authorities']) \
                           .default({'id': slice['authority']})
                }) \
                .merge(lambda slice: {
                    'project': r.table('projects').get(slice['project']) \
                           .pluck(self.fields_short['projects']) \
                           .default({'id': slice['project']})
                }) \
                .run(self.dbconnection)
            while (yield cursor.fetch_next()):
                project = yield cursor.next()
                response.append(project)


        # GET /slices/<id>
        elif not o and id:

            if not current_user:
                self.userError('permission denied')
                return

            if self.isUrn(id):
                filter = {'id' : id}

            elif self.isHrn(id):
                filter = {'hrn': id}

            else:
                self.userError('id or hrn format error')
                return

            cursor = yield r.table('slices') \
                .pluck(self.fields['slices']) \
                .filter(filter) \
                .merge(lambda slice: {
                    'authority': r.table('authorities').get(slice['authority']) \
                       .pluck(self.fields_short['authorities']) \
                       .default({'id': slice['authority']})
                }) \
                .merge(lambda slice: {
                    'project': r.table('projects').get(slice['project']) \
                           .pluck(self.fields_short['projects']) \
                           .default({'id': slice['project']})
                }) \
                .run(self.dbconnection)
            while (yield cursor.fetch_next()):
                slice = yield cursor.next()
                response.append(slice)

    @gen.coroutine
    def post(self, id=None, o=None):
        """
        POST /slices
        { shortname: string, project: string, label: string }
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
            # Check if the user has the right to create a slice under this project
            u = yield r.table('users').get(self.current_user['id']).run(self.dbconnection)
            if data['project'] in u['pi_authorities']:
                data['authority'] = data['project']
            else:
                self.userError("your user has no rights on project: %s" % data['project'])
        except Exception:
            self.userError("not authenticated or project not specified")
            return

        try:
            event = Event({
                'action': EventAction.CREATE,
                'user': self.current_user['id'],
                'object': {
                    'type': ObjectType.SLICE,
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
    def put(self):
        """
        PUT /slices/<id>
        :return:
        """
        pass

    @gen.coroutine
    def delete(self, id, o=None):
        """
        DELETE /slices/<id>
        :return:
        """
        try:
            # Check if the user has the right to delete a slice
            s = yield r.table('slices').get(id).run(self.dbconnection)
            if not self.current_user['id'] in s['users']:
                self.userError("your user has no rights on slice: %s" % id)
        except Exception:
            self.userError("not authenticated or project not specified")
            return

        try:
            event = Event({
                'action': EventAction.DELETE,
                'user': self.current_user['id'],
                'object': {
                    'type': ObjectType.SLICE,
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
                    "error": None,
                    "debug": None
                }, cls=myJSONEncoder))
