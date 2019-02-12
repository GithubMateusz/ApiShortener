import tornado.escape
import tornado.web

from . import BaseController


class ListHandler(BaseController):
    @tornado.web.authenticated
    async def get(self):
        login = tornado.escape.xhtml_escape(self.current_user)
        find = {"login": login}
        link_list = await self.database.do_find(self.collection_link, find)
        self.render(
            "list.html",
            comment="",
            login=login,
            link_list=link_list,
            home_address=self.request.host + "/"
        )

    async def post(self):
        id_link = {"short_link": self.get_argument("short_link")}
        await self.database.do_delete_one(self.collection_link, id_link)
        await self.redirect("/list")
