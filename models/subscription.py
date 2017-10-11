from google.appengine.ext import ndb

# This is used for both subscriptions to a particular as well as general subscriptions. A general subscription to latest topics has a topic_id of 1
class Subscription(ndb.Model):
    user_id = ndb.IntegerProperty()
    topic_id = ndb.IntegerProperty()
    user_email = ndb.StringProperty()


