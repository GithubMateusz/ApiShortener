from __future__ import absolute_import
import tornado.web

from config import Config
from model import Database


class BaseController(tornado.web.RequestHandler):
    def __init__(self, application, request, database=Database(), **kwargs):
        super().__init__(application, request, **kwargs)
        self.database = database
        self.collection_user = Config.DB_USER
        self.collection_link = Config.DB_LINK

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def set_current_user(self, login):
        self.set_secure_cookie("user", login)

    def delete_current_user(self):
        self.clear_cookie("user")


from .MainHandler import MainHandler
from .LoginHandler import LoginHandler
from .LogoutHandler import LogoutHandler
from .RegistrationHandler import RegistrationHandler
from .ShortenerHandler import ShortenerHandler
from .ListHandler import ListHandler
from .EditHandler import EditHandler
from .RedirectHandler import RedirectHandler

__all__ = [
    "MainHandler",
    "LoginHandler",
    "LogoutHandler",
    "RegistrationHandler",
    "ShortenerHandler",
    "ListHandler",
    "EditHandler",
    "RedirectHandler",
]
