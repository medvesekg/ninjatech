from handlers.base import BaseHandler
from classes.CustomUser import CustomUser
from models.topic import Topic
from models.comment import Comment
from classes.CSRF import CSRF

class DeleteHandler(BaseHandler):
    def post(self, topic_id):

        # Check if there is an user and if it's either an admin or the topic author
        user = CustomUser.get_current_user(self)
        if not user:
            return self.redirect("/")
        if not user.is_current_user_admin() and not user.is_author(topic_id):
            return self.redirect("/")

        if not CSRF.validate_token(self.request.get('csrf_token')):
            return self.write("CSRF fail")

        # Delete the topic
        topic = Topic.get_by_id(int(topic_id))
        topic.deleted = True
        topic.put()

        # Also delete all comments belonging to the topic
        comments = Comment.query(Comment.topic_id == int(topic_id)).fetch()

        for comment in comments:
            comment.deleted = True
            comment.put()

        return self.redirect("/")

