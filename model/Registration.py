import re


class Registration:
    def __init__(self):
        self._login = None
        self._password = None
        self._replay_password = None
        self._find_user = None

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, login_value):
        self._login = login_value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password_value):
        self._password = password_value

    @property
    def find_user(self):
        return self._find_user

    @find_user.setter
    def find_user(self, find_user_value):
        try:
            self._find_user = find_user_value
        except TypeError:
            self._find_user = None

    @property
    def replay_password(self):
        return self._replay_password

    @replay_password.setter
    def replay_password(self, replay_password_value):
        self._replay_password = replay_password_value

    def registration_strategy(self):
        check_functions = [
            "login_is_busy",
            "short_login",
            "short_password",
            "password_capital_letter",
            "password_number",
            "login_and_password_is_the_same",
            "check_passwords"
        ]
        for check_function in check_functions:
            result = getattr(self, check_function)
            if result():
                return result()
        return "success"

    def login_is_busy(self):
        if self._find_user:
            return "Podany login jest już zajęty"
        return False

    def short_login(self):
        if len(self._login) < 5:
            return "Login musi mieć minimu 6 znaków"

    def short_password(self):
        if len(self._password) < 7:
            return "Hasło musi mieć minimu 8 znaków"

    def password_capital_letter(self):
        if re.search("[A-Z]", self._password) is None:
            return "Hasło musi mieć przynajmniej jedną wielką literę"
        return False

    def password_number(self):
        if re.search("[0-9]", self._password) is None:
            return "Hasło musi mieć przynajmniej jedną liczbę"
        return False

    def login_and_password_is_the_same(self):
        if self._login == self._password:
            return "Login i hasło nie mogą być takie samę"
        return False

    def check_passwords(self):
        if self._password != self._replay_password:
            return "Podane hasła nie są takie same"
        return False
