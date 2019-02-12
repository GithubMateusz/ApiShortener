from bson.objectid import ObjectId, InvalidId
from . import BaseController


class RedirectHandler(BaseController):
    async def get(self, uri):
        try:
            short_link = uri.strip("/")
            document = await self.database.do_find_one(
                self.collection_link,
                {"short_link": short_link}
            )
            self.redirect(document["link"])
        except TypeError:
            self.render("error.html")
