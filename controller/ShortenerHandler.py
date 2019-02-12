import tornado.escape
import tornado.web
from bson.objectid import ObjectId

from . import BaseController
from model.ShortLink import ShortLink


class ShortenerHandler(BaseController):
    @tornado.web.authenticated
    def get(self):
        link = self.get_cookie("link")
        short_link = self.get_cookie("short_link")
        self.render(
            "shortener.html",
            login=tornado.escape.xhtml_escape(self.current_user),
            link=link,
            short_link=short_link
        )

    async def post(self):
        document = ShortLink()
        document.login = tornado.escape.xhtml_escape(self.current_user)
        document.link = self.get_argument("link")
        document.private = self.get_argument("private")
        document.time = self.get_argument("time")
        document.id_link = await self.database.do_insert_one(self.collection_link, {})

        document_dictionary = document.do_dictionary()

        await self.database.do_replace_one(
            self.collection_link,
            {"_id": ObjectId(document.id_link)},
            document_dictionary
        )

        self.set_cookie("link", document.link)
        self.set_cookie("short_link", self.request.host + "/" + document.short_link)
        self.redirect("/shortener")

