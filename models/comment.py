from google.appengine.ext import ndb
from models.topic import Topic
from google.appengine.api import mail, taskqueue

class Comment(ndb.Model):
    user_email = ndb.StringProperty()
    content = ndb.TextProperty()
    topic_id = ndb.IntegerProperty()
    topic_title = ndb.StringProperty()
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    updated_at = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)

    @staticmethod
    def create_comment(user, topic_id, comment_content):
        topic = Topic.get_by_id(topic_id)

        new_comment = Comment(user_email=user.email(), content=comment_content, topic_id=topic_id,
                              topic_title=topic.title)
        new_comment.put()

        params = {
            "email" : topic.user_email,
            "topic_title": topic.title,
            "topic_id": topic.key.id()
        }

        taskqueue.add(url="/task/email-topic-author", params=params)