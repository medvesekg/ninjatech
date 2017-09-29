from handlers.base import BaseHandler
from models.topic import Topic

class MainHandler(BaseHandler):
    def get(self):

        params = {}
        topics = Topic.query(Topic.deleted == False).order(-Topic.created_at).fetch()
        params['topics'] = topics

        return self.render_template("home.html", params=params)