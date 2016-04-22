import json

import rethinkdb as r

from myslice.lib.util import myJSONEncoder
from myslice.web.rest import Api

from tornado import gen, escape

class AuthenticationHandler(Api):

    @gen.coroutine
    def post(self):
        """
        POST /authentication
        { id, pw }
        :return:
        """
        pass

