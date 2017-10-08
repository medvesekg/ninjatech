from handlers.base import BaseHandler
from models.comment import Comment
import cgi
from classes.CSRF import CSRF
from classes.CustomUser import CustomUser


class NewComment(BaseHandler):
    def post(self, topic_id):

        # Check if an user is logged in
        user = CustomUser.get_current_user(self)

        if not user or not user.is_active:
            return self.write("Please login before you're allowed to post a comment.")

        # Escape the comment, strip whitespace
        comment_content = cgi.escape(self.request.get("comment_content")).strip()

        # Check if comment is empty
        if comment_content == "":
            return self.write("Please fill out all fields.")

        # Validate CSRF token
        if not CSRF.validate_token(self.request.get('csrf_token')):
            return self.write("CSRF fail")

        # Create new comment
        Comment.create_comment(user=user, topic_id=int(topic_id), comment_content=comment_content)

        # Redirect back to current topic
        return self.redirect("/topic/view/" + str(topic_id))