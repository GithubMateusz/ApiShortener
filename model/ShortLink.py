import datetime
import string
from math import floor


class ShortLink:
    def __init__(self):
        self._login = None
        self._link = None
        self._short_link = None
        self._private = None
        self._time = None
        self._id_link = None
        self._document = None

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, login_value):
        self._login = login_value

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, link_value):
        self._link = link_value

    @property
    def short_link(self):
        return self._short_link

    @short_link.setter
    def short_link(self, short_link_value):
        self._short_link = short_link_value

    @property
    def private(self):
        return self._private

    @private.setter
    def private(self, private_value):
        self._private = private_value

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, time_value):
        self._time = time_value

    @property
    def id_link(self):
        return self._id_link

    @id_link.setter
    def id_link(self, id_link_value):
        self._id_link = str(id_link_value)

    def do_dictionary(self):
        if not self._short_link:
            self._short_link = self.create_short_link()

        self._document = {
            "login": self._login,
            "link": self._link,
            "short_link": self._short_link,
            "private": self._private,
            "time": self._time
        }

        if self._time != "no_time_link":
            self._document[self._time] = datetime.datetime.utcnow()

        return self._document

    def create_short_link(self):
        chars = string.digits + string.ascii_letters
        id_link_int = int(self._id_link[0:8] + self._id_link[18:len(self._id_link)], 16)
        chars_len = len(chars)
        result = ""
        while id_link_int >= chars_len:
            char = id_link_int % chars_len
            id_link_int = int(id_link_int / chars_len)
            result = chars[char] + result

        return chars[id_link_int] + result





