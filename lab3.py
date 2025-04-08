from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from typing import Any, TextIO
from copy import deepcopy, copy
from time import time
import os

#Zadanie 1.

class OldPrint:
    def __init__(self, brand: str, model: str) -> None:
        self.brand = brand
        self.model = model

    def print_old(self, text: str) -> str:
        print(f"Metoda print old: {text}")

class NewSystem:
    def __init__(self, brand: str, model: str) -> None:
        self.brand = brand
        self.model = model

    def print_new(self, text: str) -> str:
        print(f"Metoda print new: {text}")

class SystemAdapter:
    def __init__(self, old_print: OldPrint) -> None:
        self.old_print = old_print

    def print_old(self, text: str) -> str:
        print(f"Metoda print old: {text}")

    def print_new(self, text: str) -> str:
        print(f"Metoda print new: {text}")

old_print = OldPrint("asd", "fgh")
new_system = NewSystem("zxc", "vbn")

old_print.print_old("Halo")
new_system.print_new("Witam")
new_system_adapter = SystemAdapter(old_print)

new_system_adapter.print_new("Sprawdzam")
new_system_adapter.print_old("Sprawdzam old")

class FahrenheitSensor:
    def __init__(self, temperature: float) -> None:
        self.temperature = temperature

    def temperature_in_fahrenheit(self) -> float:
        return self.temperature

class CelsiusSensor:
    def __init__(self, temperature: float) -> None:
        self.temperature = temperature

    def temperature_in_celsius(self) -> float:
        return self.temperature

class CelsiusAdapter:
    def __init__(self, fahrenheit_temperature: FahrenheitSensor) -> None:
        self.fahrenheit_temperature = fahrenheit_temperature

    def temperature_in_fahrenheit(self) -> float:
        return self.fahrenheit_temperature.temperature_in_fahrenheit()

    def temperature_in_celsius(self) -> float:
        return (self.fahrenheit_temperature.temperature_in_fahrenheit() - 32) * 5/9

fahrenheit = FahrenheitSensor(100)
adapter = CelsiusAdapter(fahrenheit)

print(fahrenheit.temperature_in_fahrenheit())
print(adapter.temperature_in_celsius())

class PayPal:
    def __init__(self, payment: float) -> None:
        self.payment = payment

    def confirmation(self):
        return f"Payment confirmed via Paypal: {self.payment}."

class Stripe:
    def __init__(self, payment: float) -> None:
        self.payment = payment

    def confirmation(self):
        return f"Payment confirmed via Stripe: {self.payment}."

class PaymentAdapter:
    def __init__(self, payment_system, payment: float) -> None:
        self.payment_system = payment_system(payment)

    def payment_confirmation(self):
        return self.payment_system.confirmation()

paypal_adapter = PaymentAdapter(PayPal, 100)
stripe_adapter = PaymentAdapter(Stripe, 50)

print(paypal_adapter.payment_confirmation())
print(stripe_adapter.payment_confirmation())

#Zadanie 2.

class DefaultClass(ABC):
    @abstractmethod
    def role(self) -> str:
        pass

class User(DefaultClass):
    def role(self) -> str:
        return "User"

class Decorator(ABC):
    def __init__(self, obj: Any) -> None:
        self.object = obj

    @abstractmethod
    def role(self) -> str:
        pass

class AdminDecorator(Decorator):
    def role(self) -> str:
        parent_value = self.object.role()

        return f"Admin {parent_value}"

class ModeratorDecorator(Decorator):
    def role(self) -> str:
        parent_value = self.object.role()

        return f"Moderator {parent_value}"

class GuestDecorator(Decorator):
    def role(self) -> str:
        parent_value = self.object.role()

        return f"Guest {parent_value}"

user = User()
print(user.role())
decorator_admin = AdminDecorator(user)
print(decorator_admin.role())
decorator_moderator = ModeratorDecorator(user)
print(decorator_moderator.role())
decorator_guest = GuestDecorator(user)
print(decorator_guest.role())

#Zadanie 2. B

def check_form(login_check):
    def form_validation(login: str, password: str):
        if len(login) >= 30:
            raise Exception("Your login is too long!")
        elif len(login) <= 5:
            raise Exception("Your login is too short!")
        elif len(password) >= 30:
            raise Exception("Your password is too long!")
        elif len(password) <= 5:
            raise Exception("Your password is too short!")
        else:
            return login_check
    return form_validation

@check_form
def login_check(login: str, password: str):
    print(login, password)

login_check("login1", "passasd")

#Zadanie 2. C

def timeit(fn: callable) -> callable:
    def wrapper(*args: list) -> str:
        start = time()
        result = fn(*args)
        stop = time()

        print(stop - start)

        return result

    return wrapper

class Database:
    @timeit
    def connection(self) -> str:
        return "Connected to database."

database = Database()
print(database.connection())

#Zadanie 3. A

class FileOpen:
    def open_file(self, file_path: str, mode: str) -> TextIO:
        return open(file_path, mode)

class FileClose:
    def close_file(self, file: str):
        file.close()

class FileWrite:
    def __init__(self, open: FileOpen, close: FileClose) -> None:
        self.open = open
        self.close = close

    def write_file(self, file_path: str, text: str) -> None:
        file = self.open.open_file(file_path, "w")
        file.write(text)
        self.close.close_file(file)

class FileRead:
    def __init__(self, open: FileOpen, close: FileClose) -> None:
        self.open = open
        self.close = close

    def read_file(self, file_path: str) -> str:
        file = self.open.open_file(file_path, "r")
        text = file.read()
        self.close.close_file(file)
        return text

class FileDelete:
    def delete_file(self, file_path: str) -> None:
        os.remove(file_path)

class FacadeFileManager:
    def __init__(self) -> None:
        open = FileOpen()
        close = FileClose()
        self.write = FileWrite(open, close)
        self.read = FileRead(open, close)
        self.delete = FileDelete()

    def file_write(self, file_path: str, text: str) -> None:
        self.write.write_file(file_path, text)
        print("Zapisano do pliku.")

    def file_read(self, file_path: str) -> str:
        return f'Czytam z pliku: {self.read.read_file(file_path)}'

    def file_delete(self, file_path: str) -> None:
        self.delete.delete_file(file_path)
        print("Usunięto plik.")


file_path_facade = "test2.txt"

facade = FacadeFileManager()

facade.file_write(file_path_facade, "Test2")

print(facade.file_read(file_path_facade))

facade.file_delete(file_path_facade)
