from handlers.base import BaseHandler
from google.appengine.api import mail


class SendMailWorker(BaseHandler):
    def post(self):

        email = self.request.get("email")
        topic_title = self.request.get("topic_title")
        topic_id = self.request.get("topic_id   ")
        mail.send_mail(sender="admin@ninjatech.com",
                       to=email,
                       subject="Nov komentar",
                       body="Tvoja tema {0} ima nov komentar. <a href='{1}'>{0}</a> \n\n Lep pozdrav".format(
                           topic_title, topic_id))
