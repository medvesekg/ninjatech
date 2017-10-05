from handlers.base import BaseHandler
from models.comment import Comment
from models.topic import Topic
from models.session import Session
from classes.CustomUser import CustomUser
from google.appengine.api import users
from models.user import User
import cgi
from classes.CSRF import CSRF

class NewComment(BaseHandler):
    def post(self, topic_id):

        user_token = self.request.cookies.get("token")
        session = Session.query(Session.token == user_token).fetch()
        user = users.get_current_user()

        if session:
            user = User.query(User.email == session[0].user_email).fetch()
            user = CustomUser(user[0].email)

        if not user:
            return self.write("Please login before you're allowed to post a topic.")


        comment_content = cgi.escape(self.request.get("comment_content")).strip()

        if comment_content == "":
            return self.write("Please fill out all fields.")

        if not CSRF.validate_token(self.request.get('csrf_token')):
            return self.write("CSRF fail")

        topic_id = int(topic_id)

        topic = Topic.get_by_id(topic_id)

        new_comment = Comment(user_email=user.email(), content=comment_content, topic_id=topic_id, topic_title=topic.title)
        new_comment.put()

        return self.redirect("/topic/view/" + str(topic_id))