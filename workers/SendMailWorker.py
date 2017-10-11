from handlers.base import BaseHandler
#from google.appengine.api import mail

import sendgrid
import os
from sendgrid.helpers.mail import *

class SendMailWorker(BaseHandler):
    def post(self):


        # email = self.request.get("email")
        # subject = self.request.get("subject")
        # body = self.request.get("body")
        # mail.send_mail(sender="admin@ninja-tech.appspotmail.com",
        #                to=email,
        #                subject=subject,
        #                body=body)




        sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email("admin@ninja-tech.appspotmail.com")
        to_email = Email(self.request.get("email"))
        subject = self.request.get("subject")
        content = Content("text/plain", self.request.get("body"))
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())





