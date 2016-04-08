import json

from tornado import gen


from myslice import db
from myslice.db.model import Event
from myslice.web.rest import Api, DecimalEncoder, DateEncoder


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

        if result is None or result['skipped']:
            data = "Bad request"
            self.respond(data=data, code=400)
        
        elif result['inserted']:
            data = "sucessfully created"
            self.respond(data, code=201)
        
        elif result['replaced']:
            data = 'sucessfully updated'
            self.respond(data)
