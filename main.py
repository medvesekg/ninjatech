#!/usr/bin/env python

import webapp2

from handlers.main import MainHandler
from handlers.cookie import CookieHandler
from handlers.topic import TopicAdd
from handlers.topic import TopicDisplay
from handlers.login import LoginHandler
from handlers.register import RegisterHandler
from handlers.checkuser import CheckUser
from handlers.logout import LogoutHandler

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/set-cookie', CookieHandler),
    webapp2.Route('/topic/add', TopicAdd),
    webapp2.Route('/topic/view/<topic_id>', TopicDisplay),
    webapp2.Route('/login', LoginHandler),
    webapp2.Route('/register', RegisterHandler),
    webapp2.Route('/checkuser', CheckUser),
    webapp2.Route('/logout', LogoutHandler),
], debug=True)
