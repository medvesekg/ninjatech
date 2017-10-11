from google.appengine.ext import ndb
from models.topic import Topic
from google.appengine.api import mail, taskqueue
from models.subscription import Subscription

class Comment(ndb.Model):
    user_email = ndb.StringProperty()
    user_id = ndb.IntegerProperty()
    content = ndb.TextProperty()
    topic_id = ndb.IntegerProperty()
    topic_title = ndb.StringProperty()
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    updated_at = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)

    @staticmethod
    def create_comment(user, topic_id, comment_content):
        topic = Topic.get_by_id(topic_id)

        new_comment = Comment(user_email=user.email(), user_id=user.id, content=comment_content, topic_id=topic_id,
                              topic_title=topic.title)
        new_comment.put()

        # Update topic updated_at property

        topic.put()

        # Build a list of emails to send

        email_list = []


        # Check subscriptions

        query = Subscription.query(Subscription.topic_id == topic_id).fetch()

        for entry in query:
            if entry.user_email == user.email():  # Don't send the email to the comment author
                continue
            else:
                email_list.append(entry.user_email)

        # If email list is empty do nothing
        if not email_list:
            return 0

        # Else send the emails

        for email in email_list:

            params = {
                "email" : email,
                "subject" : "New reply",
                "body" : u"A topic you follow http://ninja-tech.appspot.com/topic/view/{1} - '{0}' has a new comment.".format(topic.title, topic_id)
            }

            taskqueue.add(url="/task/email-topic-author", params=params)