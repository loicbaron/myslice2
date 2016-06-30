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