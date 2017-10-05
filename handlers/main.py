from handlers.base import BaseHandler
from models.topic import Topic
from models.comment import Comment
class MainHandler(BaseHandler):
    def get(self):

        params = {}
        topics = Topic.query(Topic.deleted == False).order(-Topic.created_at).fetch()
        params['topics'] = topics

        replies = {}
        for topic in topics:
            replies[str(topic.key.id())] = Comment.query(Comment.topic_id == topic.key.id()).count()

        params['replies'] = replies
        return self.render_template("home.html", params=params)