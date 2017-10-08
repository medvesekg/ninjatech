from handlers.base import BaseHandler
from google.appengine.api import memcache
from models.user import User

class ValidateEmail(BaseHandler):
    def get(self, token):

        user_email = memcache.get(token)

        if user_email:
            user = User.query(User.email == user_email).fetch()
            user = user[0]
            user.is_active = True
            user.put()
            return self.write("Your account has been activated.")



