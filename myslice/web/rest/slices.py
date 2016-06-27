import json

import rethinkdb as r

from myslice.lib.util import myJSONEncoder
from myslice.web.rest import Api

from tornado import gen, escape

class SlicesHandler(Api):

    @gen.coroutine
    def get(self, id=None, o=None):
        """
            - GET /slices
                (public) Slices list

            - GET /slices/<id>
                (public) Slices with <id>

            - GET /slices/<id>/(users|resources)
                (auth) Users/Resources list of the slice with <id>

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

    @gen.coroutine
    def post(self):
        """
        POST /slices
        :return:
        """
        pass

    @gen.coroutine
    def put(self):
        """
        PUT /slices/<id>
        :return:
        """
        pass

    @gen.coroutine
    def delete(self):
        """
        DELETE /slices/<id>
        :return:
        """
        pass