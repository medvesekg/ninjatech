from handlers.base import BaseHandler
from models.subscription import Subscription
from google.appengine.api import taskqueue
from models.topic import Topic
from datetime import datetime, timedelta

class SubscriptionsEmailsCron(BaseHandler):
    def get(self):

        email_list = Subscription.query(Subscription.topic_id == 1).fetch()

        recent_topics = Topic.query(Topic.created_at > datetime.now() - timedelta(days=1))

        for email in email_list:

            body = u"Here's a list of latest topics: \n"

            for topic in recent_topics:

                body += topic.title + " - " + "http://ninja-tech.appspot.com/topic/view/" + topic.title

            params = {
                "email" : email,
                "subject" : "Latest news",
                "body" : body


            }

            taskqueue.add(url="/task/send-subscription-email", params=params)
