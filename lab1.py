from collections import namedtuple
from dataclasses import dataclass, field

#Zadanie 1.
class Employee:
    first_name: str
    last_name: str
    salary: float

    def __init__(self, first_name: str, last_name: str, salary: float) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.salary = salary

    def get_full_name(self) -> str:
        return f"Nazywam się {self.first_name} {self.last_name}. Zarabiam {self.salary}."

class Manager(Employee):
    department: str

    def __init__(self, first_name: str, last_name: str, salary: float, department: str) -> None:
        super().__init__(first_name, last_name, salary)
        self.department = department

    def get_department_info(self) -> str:
        return f"Zarządzam działem {self.department}."


pracownik = Employee("Bartosz", "Purzycki", 10000)

print(pracownik.get_full_name())

manager = Manager("Jan", "Kowalski", 15000, "IT")

print(manager.get_full_name())
print(manager.get_department_info())

#Zadanie 2.

Transaction = namedtuple("Transaction", ["transaction_id", "amount", "currency"])

class BankAccount:
    balance: int

    def __init__(self, balance: int) -> None:
        self.balance = balance

    def apply_transaction(self, Transaction: Transaction):
        self.balance += Transaction.amount

Account = BankAccount(10000)
Transaction = Transaction(1, 1000, 1)

Account.apply_transaction(Transaction)
print(Account.balance)

#Zadanie 3.

# Napisać klasę Book używając dataclass,
# która zawiera title, author, year, price.
# Dodaj metodę apply_discount(),
# która obniży cenę książki o podany procent.

@dataclass(frozen=True)
class Book:
    title: str
    author: str
    year: int
    price: float

    def apply_discount(self, discount: int) -> None:
        return self.price - (self.price * (discount / 100))

Book = Book("Pani Jeziora", "Andrzej Sapkowski", 1999, 60)
print(Book.price)
print(Book.apply_discount(50))

#Zadanie 4.

#Stworzyć klasę Product jako dataclass zawierającą name, price, category,
# a następnie rozszerz ją o walidację ceny (powinna być większa od zera)
# oraz domyślną wartość category="General".

@dataclass(frozen=True)
class Product:
    name: str
    price: float
    category: str = field(default="General")

    def validation(self, price: float) -> None:
        if price <= 0:
            raise ValueError("Price should be higher than 0.")

Product1 = Product("Mleko", 5, "Nabial")
Product2 = Product("Maslo", 100)
Product3 = Product("Ser", -1)

print(Product1)
print(Product2)
print(Product3)

#Zadanie 5.

class Car:
    brand: str
    model: str
    year: int

    def __init__(self, brand: str, model: str, year: int):
        self.brand = brand
        self.model = model
        self.year = year

    def is_classic(self):
        if((2025 - self.year) > 25):
            return True
        else:
            return False

car1 = Car("Toyota", "Supra MK4", 1993)
print(car1.is_classic())
car2 = Car("BMW", "Jakies takie nowe", 2021)
print(car2.is_classic())
