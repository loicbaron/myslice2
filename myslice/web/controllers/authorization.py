from tornado import template, web
from oauth2.web import AuthorizationCodeGrantSiteAdapter, ImplicitGrantSiteAdapter
from oauth2.error import UserNotAuthenticated

from pprint import pprint

class CodeGrant(AuthorizationCodeGrantSiteAdapter, web.RequestHandler):
    """
        This adapter renders a confirmation page to confirm the authorization request.
    """

    def __init__(self, templates):
        self.templates = templates

    def render_auth_page(self, request, response, environ, scopes, client):
        page = template.Loader(self.templates)
        if (self.current_user):
            url = request.path + "?" + request.query_string
            response.body = page.load("login.html").generate(url=url)
        else:
            url = request.path + "?" + request.query_string
            response.body = page.load("login.html").generate(url=url)

        return response


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