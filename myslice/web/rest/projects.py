import json

import rethinkdb as r

from myslice.lib.util import myJSONEncoder
from myslice.web.rest import Api

from tornado import gen, escape

class ProjectsHandler(Api):

    @gen.coroutine
    def get(self):
        """
        GET /projects/[<id>]

        Project list or project with <id>

        :return:
        """

        projects = []

        # TODO: id must be a valid URN
        if id:
            result = yield r.table('projects').get(id).run(self.dbconnection)
            projects.append(result)
        else:
            cursor = yield r.table('projects').run(self.dbconnection)

            while (yield cursor.fetch_next()):
                result = yield cursor.next()
                projects.append(result)

        self.write(json.dumps({"result": projects}, cls=myJSONEncoder))

    @gen.coroutine
    def post(self):
        """
        POST /projects
        :return:
        """
        pass

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