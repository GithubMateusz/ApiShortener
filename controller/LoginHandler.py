from passlib.hash import argon2

from . import BaseController


class LoginHandler(BaseController):
    async def get(self):
        if self.current_user:
            self.redirect("/")
            return

        link_list = await self.database.do_find(
            self.collection_link,
            {'private': 'no'}
        )

        self.render(
            "index.html",
            comment="",
            login="",
            link_list=link_list,
            home_address=self.request.host + "/"
        )

    async def post(self):
        home_address = self.request.host + "/"
        login = self.get_argument("login")
        password = self.get_argument("password")

        link_list = await self.database.do_find(
            self.collection_link,
            {'private': 'no'}
        )
        user = await self.database.do_find_one(
            self.collection_user,
            {"login": login}
        )

        try:
            if argon2.verify(password, user["password"]):
                self.set_current_user(login)
                self.redirect("/")
            else:
                self.render(
                    "index.html",
                    comment="Podane hasło jest nie prawidłowe",
                    login="",
                    link_list=link_list,
                    home_address=home_address
                )
        except TypeError:
            self.render(
                "index.html",
                comment="Login lub hasło nie jest prawidłowy",
                login="",
                link_list=link_list,
                home_address=home_address
            )
