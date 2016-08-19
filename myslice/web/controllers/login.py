from passlib.hash import md5_crypt
import json
from email.utils import parseaddr
from hmac import compare_digest as compare_hash
import crypt
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

        feed = yield r.table('users') \
                        .filter({"email": email}) \
                        .merge(lambda user: {
                                'slices': r.table('slices') \
                                            .get_all(r.args(user['slices'])) \
                                            .pluck(['id', 'hrn',  'name', 'shortname']) \
                                            .coerce_to('array')
                        }) \
                        .run(self.application.dbconnection)
        yield feed.fetch_next()
        user = yield feed.next()

        ##
        # User password is not set
        # TODO: we redirect to a reset password page
        if not 'password' in user:
            self.render(self.application.templates + "/login.html", message="password is not set")
            return

        ##
        # check if password matches
        if not self.check_password(password, user['password']):
            self.render(self.application.templates + "/login.html", message="password does not match")
            return

        ##
        # user finally logged in, set cookie
        self.set_secure_cookie("user", json.dumps({
            'id': user['id'],
            'email': user['email'],
            'firstname': user.get('firstname', ''),
            'lastname': user.get('lastname', ''),
            'authority': user['authority'],
            'slices': user['slices'],
            'pi_authorities': user['pi_authorities'],
        }, cls=myJSONEncoder))

        self.redirect("/")


    def check_password(self, plain_password, encrypted_password):
        try:
            if md5_crypt.verify(plain_password, encrypted_password):
                return True

        except Exception as e:
            import traceback
            traceback.print_exc()
            return False
        # ##
        # # legacy method used to store passwords
        # if encrypted_password or encrypted_password[:12] != "" or \
        #                 crypt.crypt(plain_password, encrypted_password[:12]) == encrypted_password:
        #     return True

        return False

    ##
    # TODO: MD5 hash are not secure, should migrate bcrypt
    #
    # https://github.com/pyca/bcrypt

