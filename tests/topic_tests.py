import os
import unittest
import webapp2
import webtest

from google.appengine.ext import testbed
from google.appengine.api import memcache
from handlers.topic import TopicAdd, TopicDisplay
from handlers.delete import DeleteHandler
from models.topic import Topic
from models.user import User

class TopicTests(unittest.TestCase):
    def setUp(self):
        app = webapp2.WSGIApplication(
            [
                webapp2.Route('/topic/add', TopicAdd),
                webapp2.Route('/topic/view/<topic_id:\d+>', TopicDisplay),
                webapp2.Route('/topic/<topic_id:\d+>/delete', DeleteHandler),
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

    def test_topic_add(self):
        # Get
        get = self.testapp.get('/topic/add')
        self.assertEqual(get.status_int, 200)

        # Post
        memcache.add(key="abc123", value=True)
        params = {
            'csrf_token': 'abc123',
            'title': 'Nova tema',
            'text': 'Neka vsebina.'
        }
        response = self.testapp.post("/topic/add", params=params)

        self.assertEquals(response.status_int, 302)

        topic = Topic.query().get()
        self.assertEquals('Nova tema', Topic.title)

    def test_topic_display(self):

        topic = Topic.query().fetch()[0]

        get = self.testapp.get('/topic/view/' + str(topic.key.id()))

    def test_topic_delete(self):
        topic = Topic.query().fetch()[0]
        memcache.add(key="abc123", value=True)
        params = {
            "csrf_token": "abc123"
        }

        post = self.testapp.post("/topic/" + str(topic.key.id()) + "/delete", params=params)

        deleted_topic = Topic.get_by_id(topic.key.id())

        self.assertEqual(deleted_topic.deleted, True)


