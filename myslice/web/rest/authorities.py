import json

from pprint import pprint

import rethinkdb as r

from myslice.lib.util import myJSONEncoder
from myslice.web.rest import Api

from tornado import gen, escape

class AuthoritiesHandler(Api):

    @gen.coroutine
    def get(self, id=None, o=None):
        """
            - GET /authorities
                (public) Authorities list

            - GET /authorities/<id>
                (public) Authority with <id>

            - GET /authorities/(users|projects)
                (auth) Users/Projects list of the authority of the
                logged in user

            - GET /authorities/<id>/(users|projects)
                (auth) Users/Projects list of the authority with <id>

            :return:
            """
            
        response = []
        current_user = self.get_current_user()

        # GET /authorities
        if not id and not o:
            cursor = yield r.table('authorities') \
                            .pluck(self.fields['authorities']) \
                            .run(self.dbconnection)
            while (yield cursor.fetch_next()):
                authority = yield cursor.next()
                if authority['name'] is None:
                    authority['name'] = authority['shortname'].title()
                response.append(authority)


        # GET /authorities/<id>
        elif not o and id and self.isUrn(id):
            if not current_user:
                self.userError('permission denied')
                return

            cursor = yield r.table('authorities') \
                            .pluck(self.fields['authorities']) \
                            .filter({'id': id}) \
                            .filter(lambda authority:
                                           authority["pi_users"].contains(current_user['id'])
                                           or
                                           authority["users"].contains(current_user['id'])) \
                            .run(self.dbconnection)
            while (yield cursor.fetch_next()):
                authority = yield cursor.next()
                if authority['name'] is None:
                    authority['name'] = authority['shortname'].title()
                response.append(authority)

        # GET /authorities/(users|projects)
        elif not id and o in ['users', 'projects']:
            if not current_user:
                self.userError('permission denied')
                return

            cursor = yield r.table(o) \
                            .pluck(self.fields[o]) \
                            .filter({"authority": current_user['authority']}) \
                            .run(self.dbconnection)
            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                if 'name' in item and item['name'] is None:
                    item['name'] = item['shortname'].title()
                response.append(item)

        # GET /authorities/<id>/(users|projects)
        elif id and self.isUrn(id) and o in ['users', 'projects']:
            if o=='users':
                cursor = yield r.table(o) \
                            .pluck(self.fields[o]) \
                            .filter({"authority": id}) \
                            .merge(lambda user: {
                                'authority': r.table('authorities').get(user['authority']) \
                                                                    .pluck(self.fields_short['authorities']) \
                                                                    .default({'id' : user['authority']})
                            }) \
                            .merge(lambda user: {
                            'pi_authorities': r.table('authorities').get_all(r.args(user['pi_authorities'])) \
                                                                   .pluck(self.fields_short['authorities']) \
                                                                   .coerce_to('array')
                             }) \
                            .merge(lambda user: {
                                'projects': r.table('projects') \
                                       .get_all(r.args(user['projects'])) \
                                       .pluck(self.fields_short['projects']) \
                                       .coerce_to('array')
                            }) \
                            .merge(lambda user: {
                                'slices': r.table('slices') \
                                       .get_all(r.args(user['slices'])) \
                                       .pluck(self.fields_short['slices']) \
                                       .coerce_to('array')
                            }) \
                            .run(self.dbconnection)
            else:
                cursor = yield r.table(o) \
                            .pluck(self.fields[o]) \
                            .filter({"authority": id}) \
                            .run(self.dbconnection)
            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                if 'name' in item and item['name'] is None:
                    item['name'] = item['shortname'].title()
                response.append(item)

        else:
            self.userError("invalid request {} {}".format(id, o))
            return

        self.finish(json.dumps({"result": response}, cls=myJSONEncoder))

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
            #pprint(self.request.body)
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
