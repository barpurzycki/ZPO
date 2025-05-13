from abc import ABC, abstractmethod
from typing import Self

class Login:
    _instance: Self = None
    _connected = False

    def connect(self, login: str, password: str) -> None:
        if not self._connected:
            self.login = login
            self.password = password
            self.connection = f"Połączono z aplikacją: {self.login}"
            self._connected = True

    def __new__(cls, login: str, password: str) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connect(login, password)

        return cls._instance

class User:
    def __init__(self, login: str = None, password: str = None, email: str = None, role: str = None,
        permissions: list = None) -> None:
        self.login = login
        self.password = password
        self.email = email
        self.role = role
        self.permissions = permissions

    def __str__(self):
        return (
            f"Login: {self.login}\n"
            f"Password: {self.password}\n"
            f"Email: {self.email}\n"
            f"Role: {self.role}\n"
            f"Permissions: {self.permissions}\n"
        )

class UserBuilder(ABC):
    def __init__(self) -> None:
        self.user = User()

    def login_set(self, login):
        self.user.login = login
        return self

    def password_set(self, password):
        self.user.password = password
        return self

    def email_set(self, email):
        self.user.email = email
        return self

    @abstractmethod
    def role_set(self):
        pass

    @abstractmethod
    def permissions_set(self):
        pass

    def get_user(self) -> User:
        return self.user

class StudentBuilder(UserBuilder):
    def role_set(self):
        self.user.role = "Student"
        return self

    def permissions_set(self):
        self.user.permissions = ["view_content", "borrow_book", "reserve_book", "return_book"]
        return self

class ProfessorBuilder(UserBuilder):
    def role_set(self):
        self.user.role = "Professor"
        return self

    def permissions_set(self):
        self.user.permissions = ["view_content", "delete_user", "check_user"]
        return self

class Director:
    def __init__(self) -> None:
        self.builder = None
        self.user = None

    def create_new_user(self, login: str, password: str, email: str, role: str):
        if role == "Student":
            self.builder = StudentBuilder()
        elif role == "Professor":
            self.builder = ProfessorBuilder()
        else:
            raise ValueError("Wrong role.")

        self.builder.login_set(login)
        self.builder.password_set(password)
        self.builder.email_set(email)
        self.builder.role_set()
        self.builder.permissions_set()

        return self.builder.get_user()


director = Director()
student = director.create_new_user("LoginStudent", "PassStudent12", "student@email.com", "Student")
professor = director.create_new_user("ProfLogin", "ProfPass123", "professor@email.com", "Professor")

print(student)
print(professor)

login = Login("LoginStudent", "PassStudent12")
print(login.connection)
