from __future__ import absolute_import
import os

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.platform.asyncio
from tornado.options import define, options

from config import Config
from controller import *
from model import Database

define("port", default=3000, type=int)
define("config_env", default="dev", type=str)


class Application(tornado.web.Application):
    def __init__(self, render_handler, home, **settings):
        default = dict(
            template_path=os.path.join(os.path.dirname(__file__), "view"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret=Config.COOKIE_SEC,
            login_url=Config.LOGIN_URL,
            default_handler_class=home,
            db=Database()
        )
        super().__init__(handlers=render_handler, **{**default, **settings})


def main():
    render_handler = [
        (r"/", MainHandler,),
        (r"/login", LoginHandler),
        (r"/logout", LogoutHandler),
        (r"/registration", RegistrationHandler),
        (r"/logout", LogoutHandler),
        (r"/registration", RegistrationHandler),
        (r"/shortener", ShortenerHandler),
        (r"/list", ListHandler),
        (r"/edit", EditHandler),
        (r"/([a-zA-Z0-9]+)$", RedirectHandler),
    ]

    options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(
        Application(
            render_handler,
            MainHandler,
            debug=(options.config_env == "dev")
        )
    )
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
