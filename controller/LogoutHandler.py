from . import BaseController


class LogoutHandler(BaseController):
    def get(self):
        self.clear_cookie("link")
        self.clear_cookie("short_link")
        self.delete_current_user()
        self.redirect("/login")
