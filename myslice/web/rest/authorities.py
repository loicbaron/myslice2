import json

import rethinkdb as r

from myslice.lib.util import myJSONEncoder
from myslice.web.rest import Api

from tornado import gen, escape

class AuthoritiesHandler(Api):

    @gen.coroutine
    def get(self, id=None, o=None):
        """
            GET /authorities/[<id>[/(users|projects)]]

            Authority list or authority with <id>
            User or Slice list part of authority with <id>

            :return:
            """

        authority = None
        response = []

        if id:
            # get the project
            cursor = yield r.table('authorities').filter({'id': id}).filter(lambda authority:
                                                                        authority["pi_users"].contains(
                                                                             self.get_current_user_id())
                                                                          or
                                                                        authority["users"].contains(
                                                                            self.get_current_user_id())
                                                                        ).run(self.dbconnection)

            while (yield cursor.fetch_next()):
                authority = yield cursor.next()

            if not authority:
                self.userError("no authority found or permission denied")
                return

            # GET /authority/<id>/users
            if o == 'users':
                # users in a project
                cursor = yield r.table('users').filter({"authority": id}).run(self.dbconnection)
                while (yield cursor.fetch_next()):
                    item = yield cursor.next()
                    response.append(item)

            # GET /authority/<id>/projects
            elif o == 'projects':
                # users in a project
                cursor = yield r.table('projects').filter({"authority": id}).run(self.dbconnection)

                while (yield cursor.fetch_next()):
                    item = yield cursor.next()
                    response.append(item)

            # GET /authority/<id>
            elif o is None:
                response.append(authority)

            else:
                self.userError("invalid request")
                return

        # GET /authority
        else:
            # list of projects of a user
            cursor = yield r.table('authorities').run(self.dbconnection)

            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                response.append(item)

        self.write(json.dumps({"result": response}, cls=myJSONEncoder))


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