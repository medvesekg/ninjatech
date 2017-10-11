from handlers.base import BaseHandler
from models.subscription import Subscription
from google.appengine.api import taskqueue
from models.topic import Topic
from datetime import datetime, timedelta

class SubscriptionsEmailsCron(BaseHandler):
    def get(self):

        # Get all forum subscription. Topic id of 1 means general subscriptions to latest topics.
        subscriptions = Subscription.query(Subscription.topic_id == 1).fetch()

        # Build an email list
        email_list = []
        for subscription in subscriptions:
            email_list.append(subscription.user_email)

        # Get topics that were active in the past day
        recent_topics = Topic.query(Topic.updated_at > datetime.now() - timedelta(days=1))


        # Send email to each address in the list
        for email in email_list:

            body = u"Here's a list of recent hot topics: " + "\n"

            # List all active topics in each email
            for topic in recent_topics:

                body += topic.title + u" - " + u"http://ninja-tech.appspot.com/topic/view/" + str(topic.key.id()) + "\n "

            params = {
                "email" : email,
                "subject" : "Latest news",
                "body" : body


            }

            taskqueue.add(url="/task/send-subscription-email", params=params)
