import json

import rethinkdb as r
from tornado import gen

from myslice.web.rest import Api, DecimalEncoder, DateEncoder

from myslice import db
from myslice.db.model import Event
from myslice.web.rest import Api, DecimalEncoder, DateEncoder
from myslice.web.rest import Api
from myslice.lib.util import DecimalEncoder, DateEncoder


def json_encode(obj):
    return json.dumps(obj, cls=DecimalEncoder, default=DateEncoder)

class GenericHandler(Api):

    _entity = None

    def respond(self, data, code=200):
        self.set_status(200)
        self.write(json_encode({
                    "status": code,
                    "data": data
                    # errors
                    }))
        self.finish()

    @gen.coroutine
    def get(self, entity_id):
        
        results = []
        # XXX Security

        # interact with database
        if entity_id:
            item = yield db.get(
                            c = self.dbconnection, 
                            table = self._entity, 
                            id = entity_id
                        )
            results = item
        else:
            cursor = yield db.get(
                                c = self.dbconnection, 
                                table = self._entity
                                )

            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                results.append(item)

        # return status code
        if not results:
            data = "%s not found, Please check the URI." % self._entity
            self.respond(data=data, code=404)
        else:
            self.respond(data=results)

    @gen.coroutine
    def delete(self, entity_id):
        # XXX Authecitaion

        result = None

        # interact with database
        if entity_id:
            result = yield db.delete(
                            c = self.dbconnection,
                            table = self._entity,
                            id = entity_id
                            )
        
        # return status code
        if result['skipped'] or result is None:
            self.respond(data="ID not found or invalid.", code=404)
        else:
            self.respond(data="sucessfully deleted")


    @gen.coroutine
    def post(self, entity_id):
        # XXX Authecitaion

        result = None

        if entity_id:
            # interact with database
            self.respond('Method not Allowed', 405)
        
        data = { k: self.get_argument(k) for k in self.request.arguments}

        # return status code
        if result is None or result['skipped']:
            data = "Bad request"
            self.respond(data=data, code=400)
        
        # no conflict if insert conflict option 'update' enabled
        # elif result['errors']:
        #     self.set_status(409)
        #     self.finish(post_data.update({'reason':result['first_error']}))
        
        elif result['inserted']:
            self.set_status(201)
            self.finish(json.dumps({'result': result}, cls=DecimalEncoder, default=DateEncoder))
        elif result['replaced']:
            data = 'sucessfully updated'
            self.respond(data)
