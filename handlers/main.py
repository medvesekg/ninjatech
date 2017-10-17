from handlers.base import BaseHandler
from models.topic import Topic
from models.comment import Comment

import logging

class MainHandler(BaseHandler):
    def get(self):

        params = {}
        # Get all the topics
        topics = Topic.query(Topic.deleted == False).order(-Topic.created_at).fetch(limit=20)
        params['topics'] = topics
        params['number_of_topics'] = len(topics)

        replies = {}
        # Get the reply count for each topic
        for topic in topics:
            replies[str(topic.key.id())] = Comment.query(Comment.topic_id == topic.key.id()).count()

        params['replies'] = replies
        return self.render_template("home.html", params=params)