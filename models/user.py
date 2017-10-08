from google.appengine.ext import ndb

class User(ndb.Model):
    email = ndb.StringProperty()
    password = ndb.TextProperty()
    is_admin = ndb.BooleanProperty(default=False)
    is_active = ndb.BooleanProperty(default=False)
    created_at = ndb.DateTimeProperty(auto_now_add=True)