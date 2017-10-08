from handlers.base import BaseHandler
from google.appengine.api import mail

class SendMailWorker(BaseHandler):
    def post(self):

        email = self.request.get("email")
        subject = self.request.get("subject")
        body = self.request.get("body")
        mail.send_mail(sender="admin@ninja-tech.appspotmail.com",
                       to=email,
                       subject=subject,
                       body=body)



