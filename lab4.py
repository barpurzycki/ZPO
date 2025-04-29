from abc import ABC, abstractmethod
from random import choice
from typing import Self, Any
import numpy as np


#Zadanie 1. A

class Strategy(ABC):
    @abstractmethod
    def taxed_value(self, price: float) -> float:
        pass

class PolandVAT(Strategy):
    def taxed_value(self, price: float) -> float:
        return price * 1.23

class AustriaVAT(Strategy):
    def taxed_value(self, price: float) -> float:
        return price * 1.2

class HungaryVAT(Strategy):
    def taxed_value(self, price: float) -> float:
        return price * 1.27

class CountryVATChooser:
    def __init__(self, strategy: Strategy = None) -> None:
        self.strategy = strategy

    def set_strategy(self, strategy: Strategy) -> None:
        self.strategy = strategy

    def calculated_taxed_value(self, price: float) -> float:
        return self.strategy.taxed_value(price)

price = 100
strategy_chooser = CountryVATChooser()

strategy_chooser.set_strategy(PolandVAT())

print(f"Poland VAT: {strategy_chooser.calculated_taxed_value(price)}")

strategy_chooser.set_strategy(AustriaVAT())

print(f"Austria VAT: {strategy_chooser.calculated_taxed_value(price)}")

strategy_chooser.set_strategy(HungaryVAT())

print(f"Hungary VAT: {strategy_chooser.calculated_taxed_value(price)}")

#Zadanie 2. A

class Iterator:
    def __init__(self, vector: int) -> None:
        self.vector = vector
        self.index = len(vector) - 1

    def __iter__(self) -> Self:
        return self

    def __next__(self):
        if self.index < 0:
            raise StopIteration
        value = self.vector[self.index]
        self.index -= 1
        return value

list = [10, 20, 30, 40, 50]

vector = np.array(list)

print(vector)

for value in Iterator(vector):
    print(value)

#Zadanie 7. A

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
            observer.notify(currency=self, *args, **kwargs)

class Observer(ABC):
    def __init__(self, observable: Observable) -> None:
        observable.add_observer(self)

    @abstractmethod
    def notify(self, *args, **kwargs) -> None:
        pass

class Currency(Observable):
    name: str
    rate: float

    def __init__(self, name: str, rate: float) -> None:
        super().__init__()
        self.name = name
        self.rate = rate

    def update_rate(self, new_rate: float):
        if new_rate != self.rate:
            self.rate = new_rate
            self.notify(new_rate=new_rate)

class User(Observer):
    def __init__(self, name: str, observable: Observable) -> None:
        super().__init__(observable)
        self.name = name

    def notify(self, *args, **kwargs) -> None:
        currency = kwargs.get("currency")
        new_rate = kwargs.get("new_rate")
        print(f"Uwaga {self.name}, Waluta {currency.name} zmieniła kurs na {new_rate}")

usd = Currency("USD", 3.9)
eur = Currency("EUR", 4.3)

user1 = User("Bartosz", usd)
user2 = User("Dawid", eur)
user3 = User("Szymon", usd)

eur.update_rate(4.4)
usd.update_rate(3.8)
