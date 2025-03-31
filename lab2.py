from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from typing import Any
from copy import deepcopy, copy

#Zadanie 1.

print("=========== Zadanie 1 ===========")

class Pizza:
    def __init__(self) -> None:
        self.ingredients = []

    def add_ingredient(self, ingredient: str):
        self.ingredients.append(ingredient)

    def __str__(self):
        return f"Ingredients: {self.ingredients}"

class PizzaBuilder(ABC):

    def __init__(self) -> None:
        self.pizza = Pizza()

    @abstractmethod
    def add_cheese(self):
        pass

    @abstractmethod
    def add_ham(self):
        pass

    @abstractmethod
    def add_salami(self):
        pass

    @abstractmethod
    def add_onion(self):
        pass

    @abstractmethod
    def add_mushroom(self):
        pass

    def get_pizza(self) -> Pizza:
        return self.pizza

class VegetarianPizzaBuilder(PizzaBuilder):

    def add_cheese(self):
        self.pizza.add_ingredient("Ser")

    def add_onion(self):
        self.pizza.add_ingredient("Cebula")

    def add_mushroom(self):
        self.pizza.add_ingredient("Pieczarki")

    def add_ham(self):
        pass

    def add_salami(self):
        pass

class MeatPizzaBuilder(PizzaBuilder):

    def add_cheese(self):
        self.pizza.add_ingredient("Ser")

    def add_ham(self):
        self.pizza.add_ingredient("Szynka")

    def add_salami(self):
        self.pizza.add_ingredient("Salami")

    def add_onion(self):
        pass

    def add_mushroom(self):
        pass

class Director:
    def construct_vege(self, builder: PizzaBuilder):
        builder.add_cheese()
        builder.add_onion()
        builder.add_mushroom()
        return builder.get_pizza()

    def construct_meat(self, builder: PizzaBuilder):
        builder.add_cheese()
        builder.add_ham()
        builder.add_salami()
        return builder.get_pizza()

director = Director()
vege_builder = VegetarianPizzaBuilder()
vege_pizza = director.construct_vege(vege_builder)

print(vege_pizza)

meat_builder = MeatPizzaBuilder()
meat_pizza = director.construct_meat(meat_builder)

print(meat_pizza)

#Zadanie 1. C

#Klasa Computer

class Computer:
  RAM: str
  CPU: str
  GPU: str
  Motherboard: str
  Charger: str

  def __init__(self, RAM: str, CPU: str, GPU: str, Motherboard: str, Charger: str) -> None:
    self.RAM = RAM
    self.CPU = CPU
    self.GPU = GPU
    self.Motherboard = Motherboard
    self.Charger = Charger

#Klasa Computer - Builder

class Computer:
    def __init__(self) -> None:
        self.RAM = None
        self.CPU = None
        self.GPU = None
        self.Motherboard = None
        self.Charger = None

class ComputerBuilder(ABC):
    def __init__(self) -> None:
        self.computer = Computer()

    @abstractmethod
    def add_ram(self):
        pass

    @abstractmethod
    def add_cpu(self):
        pass

    @abstractmethod
    def add_gpu(self):
        pass

    @abstractmethod
    def add_motherboard(self):
        pass

    @abstractmethod
    def add_charger(self):
        pass

    def get_computer(self) -> Computer:
        return self.computer

class Director:
    def construct(self, builder: ComputerBuilder):
        builder.add_ram()
        builder.add_cpu()
        builder.add_gpu()
        builder.add_motherboard()
        builder.add_charger()
        return builder.get_computer()

print("=========== Zadanie 2 ===========")

#Zadanie 2. A

class Document(ABC):
    @abstractmethod
    def get_type(self) -> str:
        pass

class WordDocument(Document):
    def get_type(self) -> str:
        return "docx"

class PDFDocument(Document):
    def get_type(self) -> str:
        return "pdf"

class DocumentFactory:

    def create_doc(self, document_type: str) -> Document:
        if document_type == "pdf":
            return PDFDocument()
        elif document_type == "docx":
            return WordDocument()
        else:
            raise ValueError("Wrong document type.")

factory = DocumentFactory()
word = factory.create_doc("docx")
pdf = factory.create_doc("pdf")
#other_type = factory.create_doc("txt")

print(word.get_type())
print(pdf.get_type())
#print(other_type.get_type())

#Zadanie 2. B

class Animal(ABC):
    @abstractmethod
    def get_type(self) -> str:
        pass

class Cat(Animal):
    def get_type(self) -> str:
        return "Cat"

class Dog(Animal):
    def get_type(self) -> str:
        return "Dog"

class AnimalFactory:

    def create_animal(self, animal) -> Animal:
        if animal == "Cat":
            return Cat()
        if animal == "Dog":
            return Dog()
        else:
            raise ValueError(animal)

animal_factory = AnimalFactory()
animal = animal_factory.create_animal("Cat")
print(animal.get_type())

animal2 = animal_factory.create_animal("Dog")
print(animal2.get_type())

#animal3 = AnimalFactory.create_animal("Parrot")
#print(animal3.get_type())

#Zadanie 2. C

class DocumentC(ABC):
    @abstractmethod
    def get_type(self) -> str:
        pass

class WordDocumentC(Document):
    def get_type(self) -> str:
        return "docx"

class PDFDocumentC(Document):
    def get_type(self) -> str:
        return "pdf"

class DocumentFactoryC:
    _documentdict = {}

    @classmethod
    def register_doc(cls, doc_type: str, doc_class):
        cls._documentdict[doc_type] = doc_class

    @classmethod
    def create_doc(cls, doc_type: str) -> DocumentC:
        if doc_type in cls._documentdict:
            return cls._documentdict[doc_type]()
        else:
            raise ValueError("Wrong document type.")

DocumentFactoryC.register_doc("docx", WordDocumentC)
DocumentFactoryC.register_doc("pdf", PDFDocumentC)

word1 = DocumentFactoryC.create_doc("docx")
pdf1 = DocumentFactoryC.create_doc("pdf")
#txt1 = DocumentFactoryC.create_doc("txt")

print(f'Podpunkt C przykład: {word1.get_type()}')
print(f'Podpunkt C przykład: {pdf1.get_type()}')
#print(f'Podpunkt C przykład: {txt1.get_type()}')

class AnimalC(ABC):
    @abstractmethod
    def get_type(self) -> str:
        pass

class CatC(Animal):
    def get_type(self) -> str:
        return "Cat"

class DogC(Animal):
    def get_type(self) -> str:
        return "Dog"

class AnimalFactoryC:
    _animaldict = {}

    @classmethod
    def register_animal(cls, animal_type: str, animal_class):
        cls._animaldict[animal_type] = animal_class

    @classmethod
    def create_animal(cls, animal_type: str) -> AnimalC:
        if animal_type in cls._animaldict:
            return cls._animaldict[animal_type]()
        else:
            raise ValueError("Wrong animal type.")

AnimalFactoryC.register_animal("Dog", DogC)
AnimalFactoryC.register_animal("Cat", CatC)

dog1 = AnimalFactoryC.create_animal("Dog")
cat1 = AnimalFactoryC.create_animal("Cat")
#parrot = AnimalFactoryC.create_animal("Parrot")

print(f'Podpunkt C przykład: {dog1.get_type()}')
print(f'Podpunkt C przykład: {cat1.get_type()}')
#print(f'Podpunkt C przykład: {parrot.get_type()}')

class ParrotC(AnimalC):
    def get_type(self) -> str:
        return "Parrot"

AnimalFactoryC.register_animal("Parrot", ParrotC)

parrot1 = AnimalFactoryC.create_animal("Parrot")

print(f'Podpunkt C przykład: {parrot1.get_type()}')

#Zadanie 3.

print("=========== Zadanie 3 ===========")

class Car(ABC):
    @abstractmethod
    def get_info(self):
        pass

class TeslaSedan(Car):
    def get_info(self) -> str:
        return "Tesla Sedan"

class TeslaSUV(Car):
    def get_info(self) -> str:
        return "Tesla SUV"

class TeslaHatchback(Car):
    def get_info(self):
        return "Tesla Hatchback"

class BMWSedan(Car):
    def get_info(self) -> str:
        return "BMW Sedan"

class BMWSUV(Car):
    def get_info(self) -> str:
        return "BMW SUV"

class BMWHatchback(Car):
    def get_info(self):
        return "BMW Hatchback"

class CarFactory(ABC):
    @abstractmethod
    def create_sedan(self):
        pass

    @abstractmethod
    def create_suv(self):
        pass

    @abstractmethod
    def create_hatchback(self):
        pass

class TeslaFactory(CarFactory):
    def create_sedan(self) -> Car:
        return TeslaSedan()

    def create_suv(self) -> Car:
        return TeslaSUV()

    def create_hatchback(self) -> Car:
        return TeslaHatchback()

class BMWFactory(CarFactory):
    def create_sedan(self) -> Car:
        return BMWSedan()

    def create_suv(self) -> Car:
        return BMWSUV()

    def create_hatchback(self) -> Car:
        return BMWHatchback()

class AbstractFactory:
    @staticmethod
    def get_factory(model: str) -> CarFactory:
        if model == "Tesla":
            return TeslaFactory()
        elif model == "BMW":
            return BMWFactory()
        else:
            raise ValueError("Incorrect car brand")

class Client:
    def __init__(self, brand: str) -> None:
        self.factory = AbstractFactory.get_factory(brand)
        self.sedan = self.factory.create_sedan()
        self.suv = self.factory.create_suv()
        self.hatchback = self.factory.create_hatchback()

    def show_info(self):
        print(f'Sedan: {self.sedan.get_info()}')
        print(f'SUV: {self.suv.get_info()}')
        print(f'Hatchback: {self.hatchback.get_info()}')

client = Client("Tesla")
client.show_info()

client1 = Client("BMW")
client1.show_info()

#Zadanie 3. C

@dataclass
class Model:
    model: str

@dataclass
class CPU:
    cpu_name: str

@dataclass
class Memory:
    capacity: int

class Factory(ABC):
    @abstractmethod
    def produce_model(self, model: str) -> Model:
        pass

    @abstractmethod
    def produce_cpu(self, cpu_name: str) -> CPU:
        pass

    @abstractmethod
    def produce_memory(self, capacity: int) -> Memory:
        pass

class ApfelFactory(Factory):
    def produce_model(self, model: str) -> Model:
        return Model(model = model)

    def produce_cpu(self, cpu_name: str) -> CPU:
        return CPU(cpu_name = cpu_name)

    def produce_memory(self, capacity: int) -> Memory:
        return Memory(capacity = capacity)

class SzajsungFactory(Factory):
    def produce_model(self, model: str) -> Model:
        return Model(model = model)

    def produce_cpu(self, cpu_name: str) -> CPU:
        return CPU(cpu_name = cpu_name)

    def produce_memory(self, capacity: int) -> Memory:
        return Memory(capacity = capacity)

class MajFonFactory(Factory):
    def produce_model(self, model: str) -> Model:
        return Model(model = model)

    def produce_cpu(self, cpu_name: str) -> CPU:
        return CPU(cpu_name = cpu_name)

    def produce_memory(self, capacity: int) -> Memory:
        return Memory(capacity = capacity)

class AbstractFactoryPhone:
    @staticmethod
    def get_factory(brand: Any) -> Any:
        if brand == "Apfel":
            return ApfelFactory()
        elif brand == "Szajsung":
            return SzajsungFactory()
        elif brand == "MajFon":
            return MajFonFactory()
        else:
            raise ValueError("Wrong phone brand")

@dataclass
class Phone:
    model: Model
    cpu_name: CPU
    memory: Memory

class PhoneManufacturer(ABC):
    client_options: dict

    def __init__(self, client_options: dict) -> None:
        self.client_options = client_options

    def produce_phone(self) -> Phone:
        factory = AbstractFactoryPhone.get_factory(self.client_options["brand"])
        model, cpu_name, memory = self._request_parts(factory)

        return Phone(model = model, cpu_name = cpu_name, memory = memory)

    def _request_parts(self, factory: Any) -> tuple:
        model = factory.produce_model(self.client_options["model"])
        cpu_name = factory.produce_model(self.client_options["cpu_name"])
        memory = factory.produce_model(self.client_options["memory"])

        return model, cpu_name, memory

class Client:
    @staticmethod
    def request_phone(request: dict) -> Phone:
        manufacturer = PhoneManufacturer(request)
        new_phone = manufacturer.produce_phone()

        return new_phone

phone_specification = {
    "brand" : "Apfel",
    "model" : "iPhone 16 Pro",
    "cpu_name" : "Apple A18 Pro",
    "memory" : "1000"
}

client = Client()
client.request_phone(phone_specification)

#Zadanie 4.

class Character:
    def __init__(self, character_class: str) -> None:
        self.character_class = character_class

    def __str__(self) -> str:
        return f"Character class: {self.character_class}."


rogue = Character("Rogue")
print(rogue)


class Prototype:
    def __init__(self) -> None:
        self.objects = dict()

    def add_prototype(self, id_: int, obj: Any) -> None:
        self.objects[id_] = obj

    def del_prototype(self, id_: int) -> None:
        del self.objects[id_]

    def clone(self, id_: int, **kwargs: dict) -> Any:
        if id_ in self.objects:
            instance = deepcopy(self.objects[id_])

            for key in kwargs:
                setattr(instance, key, kwargs[key])

            return instance
        else:
            raise ModuleNotFoundError("ID not found!")

prototypes = Prototype()
prototypes.add_prototype("1", rogue)
another_character = prototypes.clone("1", character_class="Mage")
print(another_character)
prototypes.add_prototype("2", rogue)
another_character_2 = prototypes.clone("2", character_class="Warrior")
print(another_character_2)

#Zadanie 4. B


class CharacterB:
    def __init__(self, character_class: str, attributes: dict) -> None:
        self.character_class = character_class
        self.attributes = attributes

    def __str__(self) -> str:
        return f"Character(class={self.character_class}, attributes={self.attributes})"

class PrototypeB:
    def __init__(self) -> None:
        self.objects = dict()

    def add_prototype(self, id_: int, obj: Any) -> None:
        self.objects[id_] = obj

    def del_prototype(self, id_: int) -> None:
        del self.objects[id_]

    def deep_clone(self, id_: int, **kwargs: dict) -> Any:
        if id_ in self.objects:
            instance = deepcopy(self.objects[id_])

            for key in kwargs:
                setattr(instance, key, kwargs[key])

            return instance
        else:
            raise ModuleNotFoundError("ID not found!")

    def copy_clone(self, id_: int, **kwargs: dict) -> Any:
        if id_ in self.objects:
            instance = copy(self.objects[id_])

            for key in kwargs:
                setattr(instance, key, kwargs[key])

            return instance
        else:
            raise ModuleNotFoundError("ID not found!")

character = CharacterB("Wizard", {"strength": 5, "mana": 100})
prototypesB = PrototypeB()
prototypesB.add_prototype("1", character)

shallow_copy = prototypesB.copy_clone("1")
deep_copy = prototypesB.deep_clone("1")

character.attributes["strength"] = 10
print(f"Original: {character}")
print(f"Shallow: {shallow_copy}")
print(f"Deep: {deep_copy}")

#Zadanie 4. C

class Configuration:
    def __init__(self, language: str, file_type: str, settings: dict) -> None:
        self.language = language
        self.file_type = file_type
        self.settings = settings

    def __str__(self):
        return f"Language: {self.language}, File type: {self.file_type}, Settings: {self.settings}."


class PrototypeC:
    def __init__(self) -> None:
        self.objects = dict()

    def add_prototype(self, id_: int, obj: Any) -> None:
        self.objects[id_] = obj

    def del_prototype(self, id_: int) -> None:
        del self.objects[id_]

    def clone(self, id_: int, **kwargs: dict) -> Any:
        if id_ in self.objects:
            instance = deepcopy(self.objects[id_])

            for key in kwargs:
                setattr(instance, key, kwargs[key])

            return instance
        else:
            raise ModuleNotFoundError("ID not found!")

prototypesC = PrototypeC()
configuration = Configuration("PL", "TXT", {"width":1920, "height":1080})
prototypesC.add_prototype("1", configuration)
config_copy = prototypesC.clone("1", language="EN")
print(configuration)
print(config_copy)

#Zadanie 5.


