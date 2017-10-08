from models.session import Session
from models.user import User
from google.appengine.api import users
from models.topic import Topic
from models.subscription import Subscription

class CustomUser(object):

    def __init__(self, str_email, id, is_admin=False, is_active=True):
        self.str_email = str_email
        self.is_admin = is_admin
        self.is_active = is_active
        self.id = id


    @staticmethod
    def get_current_user(handler):

        # Check if user is logged in via google or there's a session token
        user = users.get_current_user()
        user_token = handler.request.cookies.get("token")
        session = Session.query(Session.token == user_token).fetch()


        # If there is a google user return the user
        if user:
            user_id = User.query(User.email == user.email()).fetch()[0].key.id()
            user = CustomUser(user.email(), user_id, users.is_current_user_admin())
            return user
        # If there's a session token get the user from the database and return the custom user model
        elif session:
            user = User.query(User.email == session[0].user_email).fetch()
            user = user[0]
            user = CustomUser(user.email, user.key.id(), user.is_admin, user.is_active)

            return user
        else:
            return False


    def email(self):

        return self.str_email

    def is_current_user_admin(self):

        return self.is_admin

    def is_author(self, topic_id):

        current_topic = Topic.get_by_id(int(topic_id))
        if (current_topic.user_email == self.str_email):
            return True
        else:
            return False

    def is_subscribed(self, topic_id):

        query = Subscription.query(Subscription.topic_id == int(topic_id), Subscription.user_id == self.id).fetch()
        if query:
            return True
        else:
            return False

    def delete_subscription(self, topic_id):
        query = Subscription.query(Subscription.topic_id == int(topic_id), Subscription.user_id == self.id).fetch()

        for entry in query:
            entry.key.delete()



