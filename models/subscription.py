from google.appengine.ext import ndb

class Subscription(ndb.Model):
    user_id = ndb.IntegerProperty()
    topic_id = ndb.IntegerProperty()
    user_email = ndb.StringProperty()


