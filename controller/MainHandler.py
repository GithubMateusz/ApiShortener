from __future__ import absolute_import
import tornado.escape
import tornado.web

from . import BaseController


class MainHandler(BaseController):
    @tornado.web.authenticated
    async def get(self):
        find = {'private': 'no'}
        link_list_no_private = await self.database.do_find(self.collection_link, find)
        login = tornado.escape.xhtml_escape(self.current_user)
        find_user = {'login': login, 'private': 'yes'}
        link_list_user = await self.database.do_find(self.collection_link, find_user)
        link_list = link_list_no_private + link_list_user

        self.render(
            "index.html",
            comment="",
            login=login,
            link_list=link_list,
            home_address=self.request.host + "/",
        )