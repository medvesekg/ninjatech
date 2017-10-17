from handlers.base import BaseHandler
from models.comment import Comment
import json

class LatestCommentHandler(BaseHandler):
    def get(self, topic_id):

        comments = Comment.query(Comment.topic_id == int(topic_id)).order(-Comment.created_at).fetch()
        comment = comments[0]
        comment_dict = {}
        comment_dict['content'] = comment.content
        comment_dict['email'] = comment.user_email
        data = json.dumps(comment_dict)


        return self.write(data)

