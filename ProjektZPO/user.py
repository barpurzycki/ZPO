from abc import ABC, abstractmethod

class User:
    def __init__(self, login: str = "", password: str = "", email: str = "", role: str = "",
                 permissions: list[str] = None) -> None:
        self.login = login
        self.password = password
        self.email = email
        self.role = role
        self.permissions = permissions

    def __str__(self):
        return f"Login: {self.login}, Password: {self.password}, Email: {self.email}, "\
        f"Role: {self.role}, Permissions: {self.permissions}"

class UserBuilder(ABC):
    def __init__(self) -> None:
        self.user = User()

    def set_login(self, login):
        self.user.login = login
        return self

    def set_password(self, password):
        self.user.password = password
        return self

    def set_email(self, email):
        self.user.email = email
        return self

    @abstractmethod
    def set_role(self):
        pass

    @abstractmethod
    def set_permissions(self):
        pass

    def get_user(self) -> User:
        return self.user

class StudentUserBuilder(UserBuilder):
    def set_role(self):
        self.user.role = "Student"
        return self

    def set_permissions(self):
        self.user.permissions = ["view_content", "borrow_book"]
        return self

class ProfessorUserBuilder(UserBuilder):
    def set_role(self):
        self.user.role = "Professor"
        return self

    def set_permissions(self):
        self.user.permissions = ["view_content", "add_user", "delete_user"]
        return self

class Director:
    def __init__(self) -> None:
        self.builder = None
        self.user = None

    def create_user(self, login: str, password: str, email: str, role: str) -> User:
        if role == "Student":
            self.builder = StudentUserBuilder()
        elif role == "Professor":
            self.builder = ProfessorUserBuilder()

        self.builder.set_login(login)
        self.builder.set_password(password)
        self.builder.set_email(email)
        self.builder.set_role()
        self.builder.set_permissions()

        return self.builder.get_user()

director = Director()
student_user = director.create_user("Student1", "Password123",
                                    "example_email@email.com", "Student")
professor_user = director.create_user("Professor1", "Haslo123",
                                    "example_professor_mail@email.com", "Professor")

print(student_user)
print(professor_user)
