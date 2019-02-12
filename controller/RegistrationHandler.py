from passlib.hash import argon2

from . import BaseController
from model.Registration import Registration


class RegistrationHandler(BaseController):
    def get(self):
        if self.current_user:
            self.redirect("/")
            return
        self.render(
            "registration.html",
            name="",
            login="",
            comment="",
            comment2=""
        )

    async def post(self):
        user_registration = Registration()
        user_registration.login = self.get_argument("name")
        user_registration.password = self.get_argument("password")
        user_registration.replay_password = self.get_argument("replay_password")

        find_user = await self.database.do_find_one(
            self.collection_user, {"login": user_registration.login}
        )
        if find_user:
            user_registration.find_user = find_user["login"]

        result = user_registration.registration_strategy()

        if result == "success":
            password = argon2.using(rounds=4).hash(user_registration.password)
            document = {"login": user_registration.login,
                        "password": password}
            await self.database.do_insert_one(self.collection_user, document)
            self.redirect("/login")

        self.render(
            "registration.html",
            name=user_registration.login,
            login="",
            comment="",
            comment2=result
        )
        return

