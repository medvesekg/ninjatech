from handlers.base import BaseHandler
from models.user import User
from models.comment import Comment
from models.topic import Topic

class UserProfileHandler(BaseHandler):
    def get(self, user_id):

        params = {}
        user_profile = User.get_by_id(int(user_id))
        params['user_profile'] = user_profile

        user_comments = Comment.query(Comment.user_email == user_profile.email, Comment.deleted != True).fetch()

        params['number_of_comments'] = len(user_comments)
        params['number_of_topics'] = len(Topic.query(Topic.user_email == user_profile.email, Topic.deleted != True).fetch())
        params['comments'] = user_comments


        self.render_template("userprofile.html", params=params)

class UserListHandler(BaseHandler):
    def get(self):
        params = {}

        all_users = User.query()

        params['all_users'] = all_users

        return self.render_template("userlist.html", params=params)
