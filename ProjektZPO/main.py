from abc import ABC, abstractmethod
from typing import Self

class Login:
    _instance: Self = None
    _logged: bool = False

    def __new__(cls, login: str, password: str) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connect(login, password)

        return cls._instance

    def connect(self, login: str, password: str) -> bool:
        if login in User.users_info and User.users_info[login] == password:
            print("Logged in successfully.")
            Login._logged = True
        else:
            print("Login not in database.")
            Login._logged = False

class User:
    users_info = {}
    borrowed_books = []

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

    def check_form(register):
        def form_validation(self):
            if len(self.login) >= 30:
                raise Exception("Login is too long.")
            elif len(self.login) <= 6:
                raise Exception("Login is too short.")
            elif len(self.password) >= 30:
                raise Exception("Password is too long.")
            elif len(self.password) <= 6:
                raise Exception("Password is too short.")
            else:
                return register(self)
        return form_validation

    @check_form
    def register(self):
        if self.login in User.users_info:
            print("User already exists.")
        else:
            User.users_info[self.login] = self.password
            print(f"User registered: {self.login}, {self.password}.")

    def borrow_book(self, book):
        if Login._logged == True:
            self.borrowed_books.append(book)
        else:
            print("User is not logged in.")

    def return_book(self, book):
        if Login._logged == True:
            print(f"Returned book:\n{book.title}")
            self.borrowed_books.remove(book)
        else:
            print("User is not logged in.")

    def show_borrowed_books(self):
        if Login._logged == True:
            if self.borrowed_books:
                print("Borrowed books:")
                for book in self.borrowed_books:
                    print(book.title)
        else:
            print("User is not logged in.")

    def is_book_available(self, book):
        if Login._logged == True:
            if book not in self.borrowed_books:
                print(f"Book {book.title} available.")
            else:
                print(f"Book {book.title} is not available right now.")


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

class UserDirector:
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

class Book:
    def __init__(self, title: str = None, year: int = None, author: str = None, genre: str = None) -> None:
        self.title = title
        self.year = year
        self.author = author
        self.genre = genre

    def __str__(self):
        return (f"Title: {self.title}\n"
                f"Author: {self.author}\n"
                f"Genre: {self.genre}\n"
                f"Year: {self.year}.")

class BookBuilder(ABC):
    def __init__(self) -> None:
        self.book = Book()

    def title_set(self, title):
        self.book.title = title
        return self

    def author_set(self, author):
        self.book.author = author
        return self

    def year_set(self, year):
        self.book.year = year
        return self

    @abstractmethod
    def genre_set(self, genre):
        pass

    def get_book(self):
        return self.book

class FantasyBookBuilder(BookBuilder):
    def genre_set(self, genre):
        self.book.genre = "Fantasy"
        return self

class RomanceBookBuilder(BookBuilder):
    def genre_set(self, genre):
        self.book.genre = "Romance"
        return self

class DramaBookBuilder(BookBuilder):
    def genre_set(self, genre):
        self.book.genre = "Drama"
        return self

class ComedyBookBuilder(BookBuilder):
    def genre_set(self, genre):
        self.book.genre = "Comedy"
        return self

class BookDirector:
    def __init__(self) -> None:
        self.builder = None
        self.book = None

    def add_new_book(self, title: str, year: int, author: str, genre: str):
        if genre == "Fantasy":
            self.builder = FantasyBookBuilder()
        elif genre == "Romance":
            self.builder = RomanceBookBuilder()
        elif genre == "Drama":
            self.builder = DramaBookBuilder()
        elif genre == "Comedy":
            self.builder = ComedyBookBuilder()
        else:
            raise ValueError("Wrong genre.")

        self.builder.title_set(title)
        self.builder.author_set(author)
        self.builder.year_set(year)
        self.builder.genre_set()

        return self.builder.get_book()

class BookLibrary:
    books = []

    def __init__(self):
        self._books = []

    def add_book(self, book):
        self._books.append(book)

    def delete_book(self, book):
        if book in self._books:
            self._books.remove(book)

    def edit_book(self, book, property, value):
        if book in self._books:
            if hasattr(book, property):
                setattr(book, property, value)

    def show_books(self):
        for book in self._books:
            print(book)


user_director = UserDirector()
student = user_director.create_new_user("LoginStudent", "PassStudent12", "student@email.com", "Student")

book_director = BookDirector()
library = BookLibrary()
the_witcher = book_director.add_new_book("The Witcher", 2025, "Sapkowski", "Fantasy")
harry_potter = book_director.add_new_book("Harry Potter", 1997, "J.K. Rowling", "Fantasy")
narnia = book_director.add_new_book("Narnia", 1997, "XXX", "Fantasy")

print(student)

student.register()

connect = Login("LoginStudent", "PassStudent12")

library.add_book(the_witcher)
library.add_book(harry_potter)
library.add_book(narnia)

library.edit_book(harry_potter, "year", 2000)

library.show_books()

student.borrow_book(harry_potter)
student.borrow_book(the_witcher)
student.show_borrowed_books()

student.return_book(harry_potter)
student.show_borrowed_books()

student.is_book_available(the_witcher)
student.is_book_available(harry_potter)
