from email.utils import parseaddr
from tornado.web import MissingArgumentError
from tornado import gen
from rethinkdb import r

from myslice.web.controllers import BaseController
from myslice.web.controllers.login import check_password

class Index(BaseController):

    def get(self):
        """
        Renders the login page

        :return:
        """
        self.render(self.application.templates + "/registration.html", message='')

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

        if not check_password(password, user['password']):
            self.render(self.application.templates + "/login.html", message="password does not match")
            return

        self.set_current_user(user['id'])
        self.redirect("/")



