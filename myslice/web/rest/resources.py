import json
import logging
import rethinkdb as r

from myslice.lib.util import myJSONEncoder
from myslice.web.rest import Api

from tornado import gen, escape

logger = logging.getLogger('myslice.web.rest.testbeds')

class ResourcesHandler(Api):

    @gen.coroutine
    def get(self, id=None, o=None):
        """
            - GET /resources
                (public) resources list

            - GET /resources?timestamp_start=<xxx>&timestamp_end=<xxx>
                (public) resources available within this time range

                TODO: resources available from timestamp_start
                TODO: resources available until timestamp_end
                TODO: resources reserved within this time range

            - GET /resources/<id>
                (public) Resources with <id>

            - GET /resources/<id>/leases
                Leases list of the resource with the <id>

            - GET /resources/<id>/testbeds
                Testbed of the resource with the <id>
            :return:
            """

        response = []
        current_user = self.get_current_user()

        # [?timestamp_start=<XXX>&timestamp_end=<XXX>]
        ts = self.get_argument('timestamp_start',None)
        te = self.get_argument('timestamp_end',None)

        # GET /resources
        if not id and not o and not ts and not te:
            cursor = yield r.table('resources') \
                .run(self.dbconnection)
            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                response.append(item)

        # GET /resources?timestamp_start=<XXX>&timestamp_end=<XXX>
        elif not id and not o:
            try:
                nb_leases = yield r.table("leases").count().run(self.dbconnection)
                if nb_leases > 0:
                    # Resources NOT in Leases
                    cursor = yield r.table('resources') \
                        .filter({'available':'true'}) \
                        .filter( lambda resource:
                            r.table("leases").map(lambda l:
                                l['resources'].coerce_to('array')
                            ).reduce(lambda left, right:
                                left.set_union(right)
                            ).contains(resource['id']).not_() \
                        ).run(self.dbconnection)
                    while (yield cursor.fetch_next()):
                        item = yield cursor.next()
                        response.append(item)

                    if ts and te:
                        # List of Resources ids in Leases but not in the given time range
                        in_leases = yield r.table("leases").filter(lambda l:
                            r.or_(l['start_time'].gt(int(te)),l['end_time'].lt(int(ts)))
                        ).map(lambda l:
                            l['resources'].coerce_to('array')
                        ).reduce(lambda left, right:
                            left.set_union(right)
                        ).map(lambda x:
                            r.table('resources').get(x) \
                        ).run(self.dbconnection)
                        logger.debug(in_leases)
                        response = response + in_leases

                    if ts and not te:
                        # List of Resources ids in Leases but not in the given time range
                        in_leases = yield r.table("leases").filter(lambda l:
                            l['end_time'].lt(int(ts))
                        ).map(lambda l:
                            l['resources'].coerce_to('array')
                        ).reduce(lambda left, right:
                            left.set_union(right)
                        ).map(lambda x:
                            r.table('resources').get(x) \
                        ).run(self.dbconnection)
                        response = response + in_leases

                    if not ts and te:
                        # List of Resources ids in Leases but not in the given time range
                        in_leases = yield r.table("leases").filter(lambda l:
                            l['start_time'].gt(int(te))
                        ).map(lambda l:
                            l['resources'].coerce_to('array')
                        ).reduce(lambda left, right:
                            left.set_union(right)
                        ).map(lambda x:
                            r.table('resources').get(x) \
                        ).run(self.dbconnection)
                        response = response + in_leases
                else:
                    # All available Resources (No Leases in DB)
                    cursor = yield r.table('resources') \
                        .filter({'available':'true'}) \
                        .run(self.dbconnection)
                    while (yield cursor.fetch_next()):
                        item = yield cursor.next()
                        response.append(item)
            except Exception as e:
                logger.exception(e)

        # GET /resources/<id>
        elif not o and id and self.isUrn(id):

            cursor = yield r.table('resources') \
                .filter({'id': id}) \
                .run(self.dbconnection)
            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                response.append(item)
        # GET /resources/<id>/leases
        elif id and self.isUrn(id) and o == 'leases':
            cursor = yield r.table(o) \
                .filter(lambda lease: lease["resources"].contains(id)) \
                .run(self.dbconnection)
                #

            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                response.append(item)
        # GET /resources/<id>/slices
        elif id and self.isUrn(id) and o == 'slices':
            cursor = yield r.table(o) \
                .filter(lambda slice: slice["resources"]==id) \
                .run(self.dbconnection)
                #

            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                response.append(item)
        # GET /resources/<id>/testbeds
        elif id and self.isUrn(id) and o == 'testbeds':
            cursor = yield r.table('resources') .filter({'id': id}) \
                .pluck('id','testbed','manager') \
                .merge(lambda res: {
                'testbeds': r.table('testbeds').get_all(res['testbed'], index='id') \
                       .coerce_to('array')
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
        POST /resources

        :return:
        """
        current_user = self.get_current_user()
        if not current_user:
            self.userError("not authenticated")
            return

        if not self.request.body:
            self.userError("empty request")
            return

        try:
            data = escape.json_decode(self.request.body)
        except json.decoder.JSONDecodeError as e:
            self.userError("malformed request", e.msg)
            return
        data["authority"] = self.get_current_user()['id']

    pass
    #TODO
    def delete(self, id, o=None):
        pass
    #TODO


    def put(self, id, o=None):
        pass
    #TODO
