import tornado.web
import json
import time
from pprint import pprint

class OAuth2Handler(tornado.web.RequestHandler):

    # Generator of tokens (with client authentications)
    def initialize(self, controller):
        self.controller = controller

    def post(self):
        request = self.request
        pprint(request)
        request.post_param = lambda key: json.loads(request.body.decode())[key]
        response = self.controller.dispatch(request, environ={})
        pprint(response)
        for name, value in list(response.headers.items()):
            self.set_header(name, value)

        self.set_status(response.status_code)
        self.write(response.body)


class AuthHandler(tornado.web.RequestHandler):

    def initialize(self, controller):
        self.controller = controller

    # authenticate tokens
    def prepare(self):
        try:
            token = self.get_argument('access_token', None)
            if not token:
                auth_header = self.request.headers.get('Authorization', None)
                if not auth_header:
                    raise Exception('This resource need a authorization token')
                token = auth_header[7:]

            key = 'oauth2_{}'.format(token)
            access = self.controller.access_token_store.rs.get(key)
            if access:
                access = json.loads(access.decode())
            else:
                raise Exception('Invalid Token')
            if access['expires_at'] <= int(time.time()):
                raise Exception('expired token')
        except Exception as err:
            self.set_header('Content-Type', 'application/json')
            self.set_status(401)
            self.finish(json.dumps({'error': str(err)}))
