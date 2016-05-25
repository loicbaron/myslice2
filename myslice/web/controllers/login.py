from tornado import web, escape

class BaseHandler(web.RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):

    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        name = escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name)

class Index(BaseHandler):

    def get(self):
        """
        Renders the login page

        :return:
        """
        self.render(self.application.templates + "/login.html")


    def post(self):
        """
            Authentication
        """
        self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/")



