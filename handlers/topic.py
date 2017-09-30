from handlers.base import BaseHandler
from google.appengine.api import users
from models.topic import Topic
from models.session import Session
from models.user import User
from classes.CustomUser import CustomUser


class TopicAdd(BaseHandler):
    def get(self):
        params={}
        return self.render_template("topic_add.html",params=params)

    def post(self):

        
        user_token = self.request.cookies.get("token")
        session = Session.query(Session.token == user_token).fetch()
        user = users.get_current_user()

        if session:
            user = User.query(User.email == session[0].user_email).fetch()
            user = CustomUser(user[0].email)

        if not user:
            return self.write("Please login before you're allowed to post a topic.")

        title = self.request.get("title")
        text = self.request.get("text")

        new_topic = Topic(title=title, content=text, user_email=user.email())
        new_topic.put()

        topic_id = new_topic.key.id()

        return self.redirect("/topic/view/" + str(topic_id))

class TopicDisplay(BaseHandler):
    def get(self, topic_id):

        topic = Topic.get_by_id(int(topic_id))

        params = {}
        params['topic'] = topic

        return self.render_template("topic_display.html", params=params)
