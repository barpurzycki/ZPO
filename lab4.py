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

#Zadanie 3. A

class Document(ABC):
    name: str
    content: str

    def __init__(self, name: str, content: str) -> None:
        self.name = name
        self.content = content

    @abstractmethod
    def save(self) -> str:
        pass

    @abstractmethod
    def show_content(self) -> str:
        pass

    def show_extension(self) -> str:
        pass

    def show_file(self) -> None:
        self.save()
        self.show_content()
        self.show_extension()

class PDF(Document):
    def save(self) -> str:
        print("PDF file saved.")

    def show_content(self) -> str:
        print(self.content)

    def show_extension(self) -> str:
        print("PDF File")

class DOCX(Document):
    def save(self) -> str:
        print("DOCX file saved.")

    def show_content(self) -> str:
        print(self.content)

    def show_extension(self) -> str:
        print("DOCX File")

class TXT(Document):
    def save(self) -> str:
        print("TXT file saved.")

    def show_content(self) -> str:
        print(self.content)

    def show_extension(self) -> str:
        print("TXT File")

pdf_file = PDF("PlikPDF", "To jest zawartosc pliku PDF")
docx_file = DOCX("PlikDOCX", "To jest zawartosc pliku DOCX")
txt_file = TXT("PlikTXT", "To jest zawartosc pliku TXT")

print("====")
pdf_file.show_file()
print("====")
docx_file.show_file()
print("====")
txt_file.show_file()
print("====")

#Zadanie 4.

class Memento:
    _states: list
    _i: int

    def __init__(self) -> None:
        self._states = []
        self._i = -1

    def save_state(self, state: str) -> None:
        if self._i != len(self._states) - 1:
            self._states = self._states[:self._i + 1]

        self._states.append(state)
        self._i += 1

    def undo(self) -> None:
        if self._i > 0:
            self._i -= 1

    def redo(self) -> None:
        if self._i < len(self._states) - 1:
            self._i += 1

    def read_state(self) -> str:
        return self._states[self._i]

class Settings:
    def __init__(self) -> None:
        self.settings = []
        self.memento = Memento()

    def add_setting(self, setting: str) -> None:
        self.settings.append(setting)
        self.memento.save_state(self.settings)

    def show_settings(self, show_deleted: bool = True) -> None:
        for i, setting in enumerate(self.settings):
            if not show_deleted and setting.startswith("!"):
                continue
            print(i+1, setting)

    def delete_setting(self, num: int) -> None:
        self.settings[num-1] = "!" + self.settings[num-1]
        self.memento.save_state(self.settings)

    def undo(self) -> None:
        self.memento.undo()
        self.settings = self.memento.read_state()

    def redo(self) -> None:
        self.memento.redo()
        self.settings = self.memento.read_state()

player_settings = Settings()
player_settings.add_setting("Audio 50")
player_settings.show_settings()
player_settings.add_setting("Video Quality Medium")
player_settings.add_setting("WASD movement")
player_settings.show_settings()
player_settings.delete_setting(1)
player_settings.show_settings()
player_settings.show_settings(show_deleted=False)
player_settings.undo()
player_settings.show_settings()

#Zadanie 5.

class TeamMember(ABC):
    application: str

    def process(self, application: str) -> bool | None:
        print(f"No one can do {application}. Please hire a new specialist.")

class Director(TeamMember):
    def process(self, application: str) -> bool | None:
        if "Director" in application:
            self.sign_director_application()
            return True

        return False

    @staticmethod
    def sign_director_application() -> None:
        print("Director application sign.")

class COO(TeamMember):
    def process(self, application: str) -> bool | None:
        if "COO" in application:
            self.sign_coo_application()
            return True

        return False

    @staticmethod
    def sign_coo_application() -> None:
        print("COO application sign.")

class CTO(TeamMember):
    def process(self, application: str) -> bool | None:
        if "CTO" in application:
            self.sign_cto_application()
            return True

        return False

    @staticmethod
    def sign_cto_application() -> None:
        print("CTO application sign.")

class CEO(TeamMember):
    def process(self, application: str) -> bool | None:
        if "CEO" in application:
            self.sign_ceo_application()
            return True

        return False

    @staticmethod
    def sign_ceo_application() -> None:
        print("CEO application sign.")

class Chain:
    chain: list

    def __init__(self):
        self.chain = []

    def sign_application(self, application: str) -> None:
        for link in self.chain:
            result = link.process(application)
            if result:
                break

chain_0 = Chain()

chain_0.chain.append(Director())
chain_0.chain.append(COO())
chain_0.chain.append(CTO())
chain_0.chain.append(CEO())

application = "Sign a COO application."
chain_0.sign_application(application)

application2 = "Director has to sign this application"
chain_0.sign_application(application2)
