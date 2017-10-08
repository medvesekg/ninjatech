from handlers.base import BaseHandler
from google.appengine.api import users
from models.user import User
import time

# This is only for Google login. Adds the user's email to the database if it's a new user.

class CheckUser(BaseHandler):
    def get(self):
        user = users.get_current_user()
        # Check if user is signed in
        if user:
            # If user is not already in database, write user to database
            if not User.query(User.email == user.email()).fetch():
                uporabnik = User(email=user.email(), is_active=True)

                if users.is_current_user_admin():
                    uporabnik = User(email=user.email(), is_active=True, is_admin=True)

                uporabnik.put()

            time.sleep(1)
            return self.redirect("/")