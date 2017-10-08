import os
import jinja2
import webapp2
from google.appengine.api import users
from classes.CustomUser import CustomUser

template_dir = os.path.join(os.path.dirname(__file__), "../templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False, cache_size=0)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params={}):

        # Check if cookie notice should be displayed
        piskotek = self.request.cookies.get('piskotek')
        if piskotek:
            params['piskotek'] = True

        # Check if user is logged in
        user = CustomUser.get_current_user(self)
        if user:
            params['user'] = user
            params['logout_url'] = "/logout"

        else:
            params['login_url'] = users.create_login_url('/checkuser')

        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))




