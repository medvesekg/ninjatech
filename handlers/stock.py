from handlers.base import BaseHandler
import random

class StockHandler(BaseHandler):
    def get(self):
        return self.write(random.randint(10,20))
