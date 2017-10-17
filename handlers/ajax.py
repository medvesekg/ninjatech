from handlers.base import BaseHandler
from models.comment import Comment
import json

class LatestCommentHandler(BaseHandler):
    def get(self, topic_id):

        # Find latest comment in given topic
        comments = Comment.query(Comment.topic_id == int(topic_id)).order(-Comment.created_at).fetch()
     
        # If no comments are found return this message
        if not comments:
            data = {"email": "", "content": "This topic has no comments yet."}
            return self.write(json.dumps(data))


        comment = comments[0]

        # Pass comment data to a dictionary
        comment_dict = {}
        comment_dict['email'] = comment.user_email
        comment_dict['content'] = comment.content

        # Truncate the comment's contents if too long
        if len(comment_dict['content']) > 75:
            comment_dict['content'] = comment_dict['content'][:75] + "..."

        # Convert dictionary to JSON and return
        data = json.dumps(comment_dict)
        return self.write(data)

