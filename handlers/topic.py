from handlers.base import BaseHandler

from models.topic import Topic

from models.user import User

import cgi
from models.comment import Comment
from classes.CSRF import CSRF
from classes.CustomUser import CustomUser
from models.subscription import Subscription

class TopicAdd(BaseHandler):
    def get(self):
        params={}

        csrf_token = CSRF.generate_token()
        params['csrf_token'] = csrf_token

        return self.render_template("topic_add.html",params=params)

    def post(self):

        
        user = CustomUser.get_current_user(self)

        if not user or not user.is_active:
            return self.write("Please login before you're allowed to post a topic.")

        title = cgi.escape(self.request.get("title").strip())
        text = cgi.escape(self.request.get("text").strip())

        if title == "" or text == "":
            return self.write("Please fill out all the fields.")

        if not CSRF.validate_token(self.request.get("csrf_token")):
            return self.write("CSRF fail")

        new_topic = Topic(title=title, content=text, user_email=user.email())
        new_topic.put()

        topic_id = new_topic.key.id()

        # Subscribe the author to the topic
        new_subscription = Subscription(user_id=user.id, user_email=user.email(), topic_id=topic_id)
        new_subscription.put()

        return self.redirect("/topic/view/" + str(topic_id))

class TopicDisplay(BaseHandler):
    def get(self, topic_id):

        csrf_token = CSRF.generate_token()

        topic = Topic.get_by_id(int(topic_id))

        topic_author = User.query(User.email == topic.user_email).fetch()[0]

        params = {}
        params['topic'] = topic
        params['topic_id'] = topic_id
        params['csrf_token'] = csrf_token
        params['topic_author'] = topic_author

        comments = Comment.query(Comment.topic_id == int(topic_id), Comment.deleted == False).order(Comment.created_at).fetch()

        params['comments'] = comments

        return self.render_template("topic_display.html", params=params)

class TopicSubscribe(BaseHandler):
    def get(self,topic_id):

        user = CustomUser.get_current_user(self)

        if not user:
            return self.redircet("/")

        if user.is_subscribed(topic_id):
            user.delete_subscription(topic_id)
            return self.write("You have successfuly unsubscribed from the topic")
        else:

            new_subscription = Subscription(user_id=user.id, user_email=user.email(), topic_id=int(topic_id))
            new_subscription.put()

            return self.write("You have successfuly subscribed to the topic")

