from handlers.base import BaseHandler
from models.user import User
from models.session import Session
from hashlib import sha256
import time
import cgi

class RegisterHandler(BaseHandler):
    def get(self):
        params={}
        return self.render_template("register.html", params=params)

    def post(self):

        # Get the POST data
        email = cgi.escape(self.request.get("email")).strip()
        psw = self.request.get("psw").strip()
        psw_check = self.request.get("psw_check").strip()

        # Check that no fields were submitted empty
        if email == "" or psw == "" or psw_check == "":
            return self.write("You need to fill out all the fields! Please try again!")

        # Check that passwords match
        if psw != psw_check:
            return self.write("Passwords do not match. Please try again.")

        # Check if user already exists
        if User.query(User.email == email).fetch():
            return self.write("That user already exists. Please use a different email.")

        # Hash the password
        salt = "d9be95247"
        password = sha256(salt + psw + salt).hexdigest()

        # Create new user and write to database
        new_user = User(email=email, password=password)
        new_user.put()


        #
        #  Log the user in
        #

        # Create session token
        token = sha256(str(time.time()) + new_user.email).hexdigest()

        # Write new session in database
        new_session = Session(token=token, user_email=new_user.email)
        new_session.put()

        # Write token to cookie
        self.response.set_cookie("token", token)


        return self.redirect("/")