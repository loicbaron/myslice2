import json

import rethinkdb as r
from tornado import gen

from myslice.web.rest import Api, DecimalEncoder, DateEncoder


class GenericHandler(Api):

    _entity = None

    @gen.coroutine
    def get(self, entity_id):
        
        results = []
        # XXX Security

        # interact with database
        if entity_id:
            item = yield r.table(self._entity).get(entity_id).run(self.dbconnection)
            results.append(item)
        else:
            cursor = yield r.table(self._entity).run(self.dbconnection)

            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                results.append(item)

        # return status code
        if not results:
            self.set_status(404)
            self.finish({"reason": "%s not found, Please check the URI." % self._entity})
        else:
            self.write(json.dumps({self._entity: results}, cls=DecimalEncoder, default=DateEncoder))

    @gen.coroutine
    def delete(self, slice_id):
        # XXX Authecitaion

        result = None

        # interact with database
        if slice_id:
            result = yield r.table(self._entity).get(slice_id).delete(return_changes=True).run(self.dbconnection)
        
        # return status code
        if result['skipped'] or result is None:
            self.set_status(404)
            self.finish({"reason": "ID not found or invalid."})
        else:
            self.finish(json.dumps(result, cls=DecimalEncoder, default=DateEncoder))

    @gen.coroutine
    def post(self, slice_id):
        # XXX Authecitaion

        result = None

        if not slice_id:
            # interact with database
            post_data = { k: self.get_argument(k) for k in self.request.arguments}
            if post_data['id']:
                result = yield r.table(self._entity).insert(post_data, conflict='update').run(self.dbconnection)
            else:
                #generate a new url path for resources
                pass

        # return status code
        if result is None or result['skipped']:
            self.set_status(400)
            self.finish({'reason':'Bad Request'})
        
        # no conflict if insert conflict option 'update' enabled
        # elif result['errors']:
        #     self.set_status(409)
        #     self.finish(post_data.update({'reason':result['first_error']}))
        
        elif result['inserted']:
            self.set_status(201)
            self.finish(json.dumps({'result': result}, cls=DecimalEncoder, default=DateEncoder))
        elif result['replaced']:
            self.finish(json.dumps({'status': 'sucessfully updated'}, cls=DecimalEncoder, default=DateEncoder))


    @gen.coroutine
    def put(self, slice_id):
        pass 
