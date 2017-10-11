from handlers.base import BaseHandler
from models.subscription import Subscription
from classes.CustomUser import CustomUser

class SubscriptionHandler(BaseHandler):
    def get(self):

        user = CustomUser.get_current_user(self)

        if not user:
            return self.redirect("/")

        existing_subscription =  Subscription.query(Subscription.user_id == user.id, Subscription.topic_id == 1).fetch()
        if existing_subscription:
            existing_subscription[0].key.delete()
            return self.write("You have been unsubscribed.")




        new_subscription = Subscription(user_id=user.id, topic_id = 1, user_email = user.email())
        new_subscription.put()

        return self.write("You have successfuly subscribed.")
