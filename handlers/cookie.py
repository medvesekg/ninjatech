from handlers.base import BaseHandler

class CookieHandler(BaseHandler):
    def post(self):

        self.response.set_cookie("piskotek", "nastavljen") # self.response.set_cookie(ime_piskotka, vrednost_piskotka)

        return self.redirect('/')