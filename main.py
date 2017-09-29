#!/usr/bin/env python

import webapp2

from handlers.main import MainHandler
from handlers.cookie import CookieHandler
from handlers.topic import TopicAdd
from handlers.topic import TopicDisplay

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/set-cookie', CookieHandler),
    webapp2.Route('/topic/add', TopicAdd),
    webapp2.Route('/topic/view/<topic_id>', TopicDisplay),
], debug=True)
