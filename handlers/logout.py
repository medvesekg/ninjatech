from handlers.base import BaseHandler
from models.session import Session
from classes.CustomUser import CustomUser
from google.appengine.api import users

class LogoutHandler(BaseHandler):
    def get(self):

        user = CustomUser.get_current_user(self)

        # If not logged in, redirect
        if not user:
            self.redirect("/")

        # If there is a cookie, delete it and delete the session entry in database
        user_token = self.request.cookies.get("token")
        session = Session.query(Session.token == user_token).fetch()

        if session:
            session[0].key.delete()
            self.response.delete_cookie("token")
            return self.redirect("/")

        # Else if it's a google user, redirect to the logout url
        else:
            logout_url = users.create_logout_url("/")
            return self.redirect(logout_url)

