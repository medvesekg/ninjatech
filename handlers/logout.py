from handlers.base import BaseHandler
from models.session import Session


class LogoutHandler(BaseHandler):
    def get(self):
        user_token = self.request.cookies.get("token")
        session = Session.query(Session.token == user_token).fetch()

        if session:
            session[0].key.delete()
            self.response.delete_cookie("token")
            return self.redirect("/")

