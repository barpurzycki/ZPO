from abc import ABC, abstractmethod

class Book:
    def __init__(self, title: str = None, year: int = None, author: str = None, genre: str = None) -> None:
        self.title = title
        self.year = year
        self.author = author
        self.genre = genre

    def __str__(self):
        return (f"Book:\n"
                f"Title: {self.title}\n"
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
    def genre_set(self):
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

class Director:
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

director = Director()
the_witcher = director.add_new_book("The Witcher", 2025, "Sapkowski", "Fantasy")

print(the_witcher)
