from tornado import web, escape
from oauth2.web import ImplicitGrantSiteAdapter
from oauth2.error import UserNotAuthenticated

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


class Authentication(ImplicitGrantSiteAdapter):
    """
        This adapter renders a confirmation page so the user can confirm the auth
        request.
    """

    CONFIRMATION_TEMPLATE = """
    <html>
        <body>
            <p>
                <a href="{url}&confirm=1">confirm</a>
            </p>
            <p>
                <a href="{url}&confirm=0">deny</a>
            </p>
        </body>
    </html>
        """

    def render_auth_page(self, request, response, environ, scopes, client):
        url = request.path + "?" + request.query_string
        response.body = self.CONFIRMATION_TEMPLATE.format(url=url)
        #self.render(self.application.templates + "/login.html", url=url)

    def authenticate(self, request, environ, scopes, client):
        if request.method == "GET":
            if request.get_param("confirm") == "1":
                return
        raise UserNotAuthenticated

    def user_has_denied_access(self, request):
        if request.method == "GET":
            if request.get_param("confirm") == "0":
                return True
        return False
