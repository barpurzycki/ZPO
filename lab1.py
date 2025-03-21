from collections import namedtuple
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import math

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

#Zadanie 6.

class ElectricVehicle:
    def fuel_type(self):
        return "electric"

class GasolineVehicle:
    def fuel_type(self):
        return "gasoline"

class HybridVehicle(ElectricVehicle, GasolineVehicle):
    def fuel_type(self):
        return "hybrid"

ev = ElectricVehicle()
gv = GasolineVehicle()
hv = HybridVehicle()

print(ev.fuel_type())
print(gv.fuel_type())
print(hv.fuel_type())

#Zadanie 7.

class Person:
    def introduce(self):
        return "I am person."

class Worker:
    def introduce(self):
        return "I am worker."

class Student:
    def introduce(self):
        return "I am student."

class WorkingStudent(Worker, Student):
    pass


person = Person()
worker = Worker()
student = Student()
ws = WorkingStudent()

print(person.introduce())
print(worker.introduce())
print(student.introduce())
print(ws.introduce())

#Zadanie 8.

class Animal:
    def make_sound(self):
        return "Some sound."

class Pet:
    def is_domestic(self):
        return True

class Dog(Animal, Pet):
    def make_sound(self):
        return "Woof, woof."

animal = Animal()
pet = Pet()
dog = Dog()

print(animal.make_sound())
print(pet.is_domestic())
print(dog.make_sound())
print(dog.is_domestic())

#Zadanie 9.

class FlyingVehicle:
    def move(self):
        return "I fly."

class WaterVehicle:
    def move(self):
        return "I sail."

class AmphibiousVehicle(FlyingVehicle, WaterVehicle):
    def __init__(self):
        self.mode = "flying"

    def set_mode(self, mode):
        if mode in ["flying", "water"]:
            self.mode = mode
        else:
            print("Invalid mode.")

    def move(self):
        if self.mode == "flying":
            return FlyingVehicle.move(self)
        if self.mode == "water":
            return WaterVehicle.move(self)

fv = FlyingVehicle()
wv = WaterVehicle()
av = AmphibiousVehicle()

print(fv.move())
print(wv.move())
print(av.move())

av.set_mode("water")
print(av.move())

av.set_mode("drive")
print(av.move())

#Zadanie 10.

class Robot:
    def operate(self):
        return "Performing task."

class AI:
    def think(self):
        return "Processing data."

class Android(Robot, AI):
    def self_learn(self):
        return "Learning."

robot = Robot()
ai = AI()
android = Android()

print(robot.operate())
print(ai.think())
print(android.operate())
print(android.think())
print(android.self_learn())

#Zadanie 11.

class TemperatureConverter:
    @staticmethod
    def celsius_to_fahrenheit(celsius):
        return (celsius * 9/5) +32

    @staticmethod
    def fahrenheit_to_celsius(fahrenheit):
        return (fahrenheit -32) * 5/9

celsius = 20
fahrenheit = TemperatureConverter.celsius_to_fahrenheit(celsius)
print(fahrenheit)

fahrenheit2 = 68
celsius2 = TemperatureConverter.fahrenheit_to_celsius(fahrenheit2)
print(celsius2)

#Zadanie 12.

class IDGenerator:
    id = 0

    def __init__(self):
        IDGenerator.id += 1
        self.id = IDGenerator.id

    @classmethod
    def generate_id(cls) -> int:
        return cls.id

id1 = IDGenerator()
id2 = IDGenerator()
id3 = IDGenerator()

print(id1.id)
print(id2.id)
print(id3.id)

#Zadanie 13.

class Store:
    total_customers = 0

    def add_customer(self):
        Store.total_customers += 1

    @classmethod
    def get_total_cutomers(cls):
        return cls.total_customers

store1 = Store()
store1.add_customer()
store1.add_customer()

print(f"Customers: {store1.get_total_cutomers()}")

#Zadanie 14.

class MathOperations:
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def multiply(a, b):
        return a * b

    @classmethod
    def identity_matrix(cls, size):
        return [[1 if i == j else 0 for j in range(size)] for i in range(size)]

math_add = MathOperations.add(4, 2)
math_multiply = MathOperations.multiply(4, 2)
math_matrix = MathOperations.identity_matrix(3)

print(math_add)
print(math_multiply)
for i in math_matrix:
    print(i)

#Zadanie 15.

class GameCharacter:
    default_health = 100

    def __init__(self) -> None:
        self.health = GameCharacter.default_health

    def restore_health(self):
        self.health = GameCharacter.default_health

    @classmethod
    def set_default_health(cls, new_health):
        cls.default_health = new_health

character1 = GameCharacter()
character2 = GameCharacter()

print(character1.health)
print(character2.health)

character1.health = 50
print(character1.health)
character1.restore_health()
print(character1.health)

GameCharacter.default_health = 200
character3 = GameCharacter()
print(character3.health)

#Zadanie 16.

class Shape(ABC):
    @abstractmethod
    def area(self) -> None:
        pass

class Circle(Shape):
    radius: int

    def __init__(self, radius: int) -> None:
        self.radius = radius

    def area(self):
        return math.pi * (self.radius ** 2)

class Rectangle(Shape):
    a: int
    b: int

    def __init__(self, a: int, b: int) -> None:
        self.a = a
        self.b = b

    def area(self):
        return self.a * self.b

circle = Circle(10)
rectangle= Rectangle(5, 3)

print(circle.area())
print(rectangle.area())

class PaymentProcessor(ABC):
    @abstractmethod
    def authorize_payment(self, amount: float) -> str:
        pass

    @abstractmethod
    def capture_payment(self, amount: float) -> str:
        pass

class CreditCardPayment(PaymentProcessor):
    def authorize_payment(self, amount: float) -> str:
        return f"Oplacono karta kredytowa, ilosc: {amount}."

    def capture_payment(self, amount: float) -> str:
        return f"Przyjeto wplate karta kredytowa, ilosc: {amount}."


class PayPalPayment(PaymentProcessor):
    def authorize_payment(self, amount: float) -> str:
        return f"Oplacono PayPal, ilosc: {amount}."

    def capture_payment(self, amount: float) -> str:
        return f"Przyjeto wplate PayPal, ilosc: {amount}."

creditcard = CreditCardPayment()
paypal = PayPalPayment()

print(creditcard.authorize_payment(100))
print(creditcard.capture_payment(100))

print(paypal.authorize_payment(200))
print(paypal.capture_payment(200))

#Zadanie 18.

class VehicleABC(ABC):
    @abstractmethod
    def max_speed(self) -> int:
        pass

class CarABC(VehicleABC):
    def __init__(self, speed: int) -> None:
        self.speed = speed

    def max_speed(self) -> int:
        return self.speed

class BicycleABC(VehicleABC):
    def __init__(self, speed: int) -> None:
        self.speed = speed

    def max_speed(self) -> int:
        return self.speed

carabc = CarABC(220)
bicycleabc = BicycleABC(35)

print(carabc.max_speed())
print(bicycleabc.max_speed())

#Zadanie 19.

class DatabaseConnection(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def execute_query(self, query: str) -> str:
        pass

class MySQLConnection(DatabaseConnection):
    def connect(self) -> None:
        return "Connected to MySQL Database."

    def execute_query(self, query: str) -> str:
        return f"Execute MySQL Query: {query}."

class PostgresSQLConnection(DatabaseConnection):
    def connect(self) -> None:
        return "Connected to PostgresSQL Database."

    def execute_query(self, query: str) -> str:
        return f"Execute PostgresSQL Query: {query}."

mysql = MySQLConnection()
postgres = PostgresSQLConnection()

print(mysql.connect())
print(postgres.connect())

print(mysql.execute_query("Select * FROM table1;"))
print(postgres.execute_query("Select * FROM table2;"))

#Zadanie 20.

class Instrument(ABC):
    @abstractmethod
    def play(self) -> str:
        pass

class Piano(Instrument):
    def play(self) -> str:
        print("Granie na pianinku.")

class Guitar(Instrument):
    def play(self) -> str:
        print("Granie na gitarce.")

piano = Piano()
guitar = Guitar()

piano.play()
guitar.play()
