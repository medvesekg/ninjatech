import os
import unittest
import webapp2
import webtest

from google.appengine.ext import testbed
from google.appengine.api import memcache
from handlers.comment import NewComment, CommentDelete
from models.topic import Topic
from models.user import User
from models.comment import Comment

class TopicTests(unittest.TestCase):
    def setUp(self):
        app = webapp2.WSGIApplication(
            [
                webapp2.Route('/new_comment/<topic_id:\d+>', NewComment),
                webapp2.Route('/comment/<comment_id:\d+>/delete', CommentDelete),
            ])

        self.testapp = webtest.TestApp(app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()

        """ Uncomment the stubs that you need to run tests. """
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # self.testbed.init_mail_stub()
        # self.testbed.init_taskqueue_stub()
        self.testbed.init_user_stub()
        # ...

        """ Uncomment if you need user (Google Login) and if this user needs to be admin. """
        os.environ['USER_EMAIL'] = 'test@example.com'
        # os.environ['USER_IS_ADMIN'] = '1'

        test_user = User(email="test@example.com", is_active=True)
        test_user.put()

        test_topic = Topic(title="test topic", content="test", user_email="test@example.com")
        test_topic.put()


    def tearDown(self):
        self.testbed.deactivate()

    def test_comment_add(self):

        # Post
        memcache.add(key="abc123", value=True)
        user = User.query().fetch()[0]
        topic = Topic.query().fetch()[0]
        params = {

            'comment_content': 'Neka vsebina.',

            'csrf_token': "abc123",
        }
        response = self.testapp.post("/new_comment/" + str(topic.key.id()), params=params)

        comment = Comment.query().get()

        self.assertEqual(comment.content, "Neka vsebina.")


    def test_comment_delete(self):
        user = User.query().get()
        topic = Topic.query().get()
        test_comment = Comment(user_email=user.email,
                               user_id=user.key.id(),
                               content="Test content",
                               topic_id=topic.key.id(),
                               topic_title=topic.title)
        test_comment.put()

        memcache.add(key="abc123", value=True)
        params = {
            "csrf_token": "abc123"
        }

        response = self.testapp.post("/comment/" + str(test_comment.key.id()) + "/delete", params=params)




