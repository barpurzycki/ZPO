from abc import ABC, abstractmethod
from typing import Self, Any


class Login:
    _instance: Self = None
    _logged: bool = False

    def __new__(cls, login: str, password: str) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connect(login, password)

        return cls._instance

    def connect(self, login: str, password: str) -> None:
        if login in User.users_info and User.users_info[login] == password:
            print("Logged in successfully.")
            Login._logged = True
        else:
            print("Login not in database.")
            Login._logged = False


class Observable(ABC):
    _observers: set

    def __init__(self) -> None:
        self._observers = set()

    def add_observer(self, observer: Any) -> None:
        self._observers.add(observer)

    def delete_observer(self, observer: Any) -> None:
        self._observers.remove(observer)

    def notify(self, *args: list, **kwargs: dict) -> None:
        for observer in self._observers:
            observer.notify(*args, **kwargs)


class Observer(ABC):
    def __init__(self, observable: Observable) -> None:
        observable.add_observer(self)

    @abstractmethod
    def notify(self, *args: list, **kwargs: dict) -> None:
        pass

class Manager(Observer):
    def notify(self, *args, **kwargs: dict) -> None:
        book = kwargs["book"]
        if book.available == True:
            print(f"You can now borrow book {book.title}.")


class User():
    users_info = {}
    borrowed_books = []
    reserved_books = []

    def __init__(self, login: str = None, password: str = None, email: str = None,
                 role: str = None, permissions: list = None) -> None:
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
            if book.borrow() == True:
                self.borrowed_books.append(book)
                print(f"You borrowed book {book.title}.")
            else:
                print(f"Book {book.title} is not available at the moment.")
        else:
            print("User is not logged in.")

    def return_book(self, book):
        if Login._logged == True:
            if book in self.borrowed_books:
                print(f"Returned book:\n{book.title}")
                self.borrowed_books.remove(book)
                book.return_book()
            else:
                print(f"You did not borrow book {book.title}.")
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
            if book.available == True:
                print(f"Book {book.title} is available.")
            else:
                print(f"Book {book.title} is not available right now.")
        else:
            print(f"User is not logged in.")

    def reserve_book(self, book):
        if Login._logged == True:
            if book.available == False:
                print(f"You reserved book {book.title}. We will inform you when it becomes available.")
                self.reserved_books.append(book)
            else:
                print(f"Book {book.title} is available, you can borrow it right now.")

    def show_reserved_books(self):
        if Login._logged == True:
            if self.reserved_books:
                print("Reserved books:")
                for book in self.reserved_books:
                    print(book.title)


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


class Book(Observable):
    def __init__(self, title: str = None, year: int = None, author: str = None, genre: str = None) -> None:
        super().__init__()
        self.title = title
        self.year = year
        self.author = author
        self.genre = genre
        self.available = True

    def __str__(self):
        return (f"Title: {self.title}\n"
                f"Author: {self.author}\n"
                f"Genre: {self.genre}\n"
                f"Year: {self.year}.")

    def return_book(self) -> None:
        self.available = True
        self.notify(book=self)

    def borrow(self) -> bool:
        if self.available == True:
            self.available = False
            return True
        else:
            return False


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
    def genre_set(self):
        pass

    def get_book(self):
        return self.book


class FantasyBookBuilder(BookBuilder):
    def genre_set(self):
        self.book.genre = "Fantasy"
        return self


class RomanceBookBuilder(BookBuilder):
    def genre_set(self):
        self.book.genre = "Romance"
        return self


class DramaBookBuilder(BookBuilder):
    def genre_set(self):
        self.book.genre = "Drama"
        return self


class ComedyBookBuilder(BookBuilder):
    def genre_set(self):
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

class Memento:
    _states: list
    _i: int

    def __init__(self) -> None:
        self._states = []
        self._i = -1

    def save_state(self, state: str) -> None:
        if self._i != len(self._states) -1:
            self._states = self._states[:self._i + 1]

        self._states.append(state.copy())
        self._i += 1

    def undo_state(self) -> None:
        if self._i > 0:
            self._i -= 1

    def read_state(self) -> str:
        return self._states[self._i].copy()

class History:
    def __init__(self) -> None:
        self.operations = []
        self.memento = Memento()

    def add_operation(self, operation: str) -> None:
        self.operations.append(operation)
        self.memento.save_state(self.operations)

    def show_history(self) -> None:
        for operation in self.operations:
            print(operation)

    def undo_operation(self) -> None:
        self.memento.undo_state()
        self.operations = self.memento.read_state()

ISBN_database_record = {
    1:
        {
            'title':'Programowanie poradnik',
            'year':'2015',
            'author':'Jakiś Hindus',
            'genre':'Informatyka'
        },
    2:
        {
            'title':'Liczenie poradnik',
            'year':'2025',
            'author':'Jakiś Matematyk',
            'genre':'Matematyka'
        },
    3:
        {
            'title':'Pisanie poradnik',
            'year':'2000',
            'author':'Jakiś Humanista',
            'genre':'Polski'
        }
}

def select_from_database(table_id: int) -> None:
    selected_book = ISBN_database_record.get(table_id)
    print(f"Title: {selected_book['title']}\n"
          f"Year: {selected_book['year']}\n"
          f"Author: {selected_book['author']}\n"
          f"Genre: {selected_book['genre']}.")


user_director = UserDirector()
book_director = BookDirector()
library = BookLibrary()

student = user_director.create_new_user("LoginStudent", "PassStudent12", "student@email.com", "Student")

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

student.reserve_book(the_witcher)
student.reserve_book(harry_potter)

manager = Manager(the_witcher)

student.return_book(the_witcher)
