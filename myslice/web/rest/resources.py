import json

import rethinkdb as r
from tornado import gen

from myslice.web.rest import Api
from myslice.lib.util import myJSONEncoder


class ResourcesHandler(Api):

    @gen.coroutine
    def get(self, id=None, o=None):
        """
        GET /resources/[<id>]

        Resource list or resource with <id>

        GET /resources/<id>/leases

        leases list with resourse id
        :return:
        """
        resources = []

        # TODO: id must be a valid URN
        if not id and not o:
            cursor = yield r.table('resources').run(self.dbconnection)
            while (yield cursor.fetch_next()):
                result = yield cursor.next()
                resources.append(result)
        elif id:
            result = yield r.table('resources').get(id).run(self.dbconnection)
            resources.append(result)




        #  GET /resources/<id>/leases
        elif self.isUrn(id) and o == 'leases':
            cursor = yield r.table(o).filter(lambda lease: lease["manager"] == id).run(self.dbconnection)


            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                resources.append(item)
        else :
             self.userError("invalid request")
             return
        self.write(json.dumps({"result": resources}, cls=myJSONEncoder))