from handlers.base import BaseHandler
from models.user import User
from models.session import Session
from hashlib import sha256
import time

class LoginHandler(BaseHandler):
    def get(self):
        return self.render_template("login.html")

    def post(self):

        # Get POST data
        email = self.request.get("email")
        password = self.request.get("psw")

        # Check if user exists
        user = User.query(User.email == email).fetch()
        if not user:
            return self.write("Email or password is wrong")

        # Compare hashed password with value in database
        salt = "d9be95247"
        password = sha256(salt + password + salt).hexdigest()
        if password != user[0].password:
            return self.write("Email or password is wrong")

        # Create session token
        token = sha256(str(time.time()) + user[0].email).hexdigest()

        # Write new session in database
        new_session = Session(token=token, user_email=user[0].email)
        new_session.put()

        # Write token to cookie
        self.response.set_cookie("token", token)

        return self.redirect("/")

