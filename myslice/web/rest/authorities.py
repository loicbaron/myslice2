import json

import rethinkdb as r

from myslice.lib.util import myJSONEncoder
from myslice.web.rest import Api

from tornado import gen, escape

class AuthoritiesHandler(Api):

    @gen.coroutine
    def get(self, id=None):
        """
        GET /authorities/[<id>]

        Authorities list or authority with <id>

        :return:
        """
        authorities = []

        # TODO: id must be a valid URN
        if id:
            result = yield r.table('authorities').get(id).run(self.dbconnection)
            authorities.append(result)
        else:
            cursor = yield r.table('authorities').run(self.dbconnection)

            while (yield cursor.fetch_next()):
                result = yield cursor.next()
                authorities.append(result)

        self.write(json.dumps({"result": authorities}, cls=myJSONEncoder))

    @gen.coroutine
    def post(self):
        """
        POST /authorities
        { 'name': 'Test Authority', 'shortname': 'test_authority' }
        :return:
        """


        payload = {
            "event": {
                "action": "CREATE",
                "user": "urn:publicid:IDN+onelab:upmc+user+loic_baron",
                "object": {
                    "type": "AUTHORITY",
                    "id": "urn:publicid:IDN+onelab:test_authority+authority+sa"
                },
                "data": {
                    "name": "Test Autority",
                    "pi_users": ["urn:publicid:IDN+onelab:upmc+user+loic_baron"]
                }
            }
        }

        try:
            data = escape.json_decode(self.request.body)['event']
        except json.decoder.JSONDecodeError as e:
            #pprint(self.request.body)
            import traceback
            traceback.print_exc()
            self.set_status(400)
            self.finish(json.dumps({"return": {"status": "error", "messages": "malformed request"}}))
            return

        try:
            event = Event(data)
        except Exception as e:
            pprint(self.request.body)
            import traceback
            traceback.print_exc()
            self.set_status(500)
            self.finish(json.dumps({"return": {"status": "error", "messages": e.message}}))

    @gen.coroutine
    def put(self):
        """
        PUT /authorities/<id>
        :return:
        """
        pass

    @gen.coroutine
    def delete(self):
        """
        DELETE /authorities/<id>
        :return:
        """
        pass