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

        id = 'urn:publicid:IDN+onelab:upmc+user+loic_baron'

        user = yield r.table('users').get(id).run(self.application.dbconnection)
        if not user:
            pass

        self.set_secure_cookie("user", json.dumps({
            'id': user['id'],
            'email': user['email'],
            'firstname': user.get('firstname', ''),
            'lastname': user.get('lastname', ''),
            'authority': user['authority']
        }, cls=myJSONEncoder))

        self.render(self.application.templates + "/login.html", message='')

    @gen.coroutine
    def post(self):
        """
            Authentication
        """

        try:
            post_email = self.get_argument("email")
        except MissingArgumentError as e:
            self.render(self.application.templates + "/login.html", message="email missing")
            return

        try:
            post_password = self.get_argument("password")
        except MissingArgumentError as e:
            self.render(self.application.templates + "/login.html", message="password missing")
            return

        _, email = parseaddr(post_email)
        if not email:
            self.render(self.application.templates + "/login.html", message="wrong email")
            return

        if not post_password:
            self.render(self.application.templates + "/login.html", message="empty password")
            return
        else:
            password = post_password

        feed = yield r.table('users').filter({"email" : email}).run(self.application.dbconnection)
        yield feed.fetch_next()
        user = yield feed.next()

        if not user:
            self.render(self.application.templates + "/login.html", message="user does not exist")
            return

        if not compare_hash(crypt.crypt(password, user['password']), user['password']) and not compare_legacy_password(password, user['password']):
            self.render(self.application.templates + "/login.html", message="password does not match")
            return

        self.redirect("/")

def compare_legacy_password(plain_password, stored_password):
    # Compare plaintext against encrypted password stored in the DB
    # Protect against blank passwords in the DB
    if stored_password is None or stored_password[:12] == "" or \
        crypt.crypt(plain_password, stored_password[:12]) != stored_password:
        return False
    return True
