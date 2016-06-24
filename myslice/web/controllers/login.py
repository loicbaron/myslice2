from email.utils import parseaddr
import crypt
from hmac import compare_digest as compare_hash
import json
from tornado.web import MissingArgumentError
from tornado import gen
from rethinkdb import r

from myslice.lib.util import myJSONEncoder
from myslice.web.controllers import BaseController

class Index(BaseController):

    @gen.coroutine
    def get(self):
        """
        Renders the login page

        :return:
        """

        self.render(self.application.templates + "/login.html", message='')

    @gen.coroutine
    def post(self):
        """
            Authentication
        """

        try:
            post_email = self.get_argument("email")
            post_password = self.get_argument("password")
            _, email = parseaddr(post_email)
            password = post_password
            feed = yield r.table('users').filter({"email" : email}).run(self.application.dbconnection)
            yield feed.fetch_next()
            user = yield feed.next()

            if not compare_hash(crypt.crypt(password, user['password']), user['password']) and not compare_legacy_password(password, user['password']):
                raise ValueError('password does not match')

            self.set_secure_cookie("user", json.dumps({
                'id': user['id'],
                'email': user['email'],
                'firstname': user.get('firstname', ''),
                'lastname': user.get('lastname', ''),
                'authority': user['authority']
            }, cls=myJSONEncoder))

        except Exception as e:
            self.render(self.application.templates + "/login.html", message="Invalid email or password")
            return

        self.redirect("/")

def compare_legacy_password(plain_password, stored_password):
    # Compare plaintext against encrypted password stored in the DB
    # Protect against blank passwords in the DB
    if stored_password is None or stored_password[:12] == "" or \
        crypt.crypt(plain_password, stored_password[:12]) != stored_password:
        return False
    return True
