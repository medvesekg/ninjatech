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
from handlers.comment import NewComment
from workers.SendMailWorker import SendMailWorker

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/set-cookie', CookieHandler),
    webapp2.Route('/topic/add', TopicAdd),
    webapp2.Route('/topic/view/<topic_id:\d+>', TopicDisplay),
    webapp2.Route('/login', LoginHandler),
    webapp2.Route('/register', RegisterHandler),
    webapp2.Route('/checkuser', CheckUser),
    webapp2.Route('/logout', LogoutHandler),
    webapp2.Route('/new_comment/<topic_id:\d+>', NewComment),
    webapp2.Route('/task/email-topic-author', SendMailWorker)
], debug=True)
