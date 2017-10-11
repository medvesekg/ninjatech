from datetime import datetime, timedelta

from handlers.base import BaseHandler
from models.topic import Topic
from models.comment import Comment


class DeleteTopicsCron(BaseHandler):
    def get(self):

        month_ago = datetime.now() - timedelta(days=30)
        topics = Topic.query(Topic.deleted == True, Topic.created_at <= month_ago).fetch()

        for topic in topics:

            comments = Comment.query(Comment.topic_id == topic.key.id()).fetch()

            for comment in comments:
                comment.key.delete()


            topic.key.delete()


        comments = Comment.query(Comment.deleted == True, Comment.created_at <= month_ago).fetch()

        for comment in comments:
            comment.key.delete()


