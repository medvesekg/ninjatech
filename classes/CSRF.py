import uuid
from google.appengine.api import memcache

class CSRF(object):

    @staticmethod
    def generate_token():
        csrf_token = str(uuid.uuid4())
        memcache.add(csrf_token, True, time=3600)
        return csrf_token

    @staticmethod
    def validate_token(csrf_token):
        if memcache.get(csrf_token):
            return True
        else:
            return False
