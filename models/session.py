from google.appengine.ext import ndb

class Session(ndb.Model):
    user_email = ndb.StringProperty()
    token = ndb.StringProperty()