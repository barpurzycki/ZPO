from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from typing import Any
from copy import deepcopy, copy

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
