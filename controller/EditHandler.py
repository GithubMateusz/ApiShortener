import tornado.escape
import tornado.web

from . import BaseController
from model.ShortLink import ShortLink


class EditHandler(BaseController):
    @tornado.web.authenticated
    async def get(self):
        find_link = {"short_link": self.get_argument("short_link")}
        document = await self.database.do_find_one(self.collection_link, find_link)
        await self.render(
            "edit.html",
            login=tornado.escape.xhtml_escape(self.current_user) ,
            comment="",
            short_link=self.get_argument("short_link"),
            link=document["link"],
            time=document["time"],
            typ=document["private"],
            home_address=self.request.host + "/",
        )

    async def post(self):
        link = {"short_link": self.get_argument("short_link")}

        document = ShortLink()
        document.login = tornado.escape.xhtml_escape(self.current_user)
        document.link = self.get_argument("link")
        document.short_link = self.get_argument("short_link")
        document.private = self.get_argument("private")
        document.time = self.get_argument("time")

        document_dictionary = document.do_dictionary()

        await self.database.do_replace_one(
            self.collection_link,
            link,
            document_dictionary)

        self.redirect("/list")
