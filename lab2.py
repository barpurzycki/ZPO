from abc import ABC, abstractmethod

#Zadanie 1.

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

#Zadanie 2.

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

#Zadanie 2. A

class Document(ABC):
    @abstractmethod
    def get_type(self) -> str:
        pass

class DocumentFactory(ABC):
    @abstractmethod
    def create_doc(self) -> Document:
        pass

class WordDocument(Document):
    def get_type(self) -> str:
        return "doc"

class PDFDocument(Document):
    def get_type(self) -> str:
        return "pdf"

class WordDocumentFactory(DocumentFactory):
    def create_doc(self) -> Document:
        return WordDocument()

class PDFDocumentFactory(DocumentFactory):
    def create_doc(self) -> Document:
        return PDFDocument()

word_factory = WordDocumentFactory()
pdf_factory = PDFDocumentFactory()

word = word_factory.create_doc()
pdf = pdf_factory.create_doc()

print(word.get_type())
print(pdf.get_type())

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

    def create_animal(animal) -> Animal:
        if animal == "Cat":
            return Cat()
        if animal == "Dog":
            return Dog()
        else:
            raise ValueError(animal)

animal = AnimalFactory.create_animal("Cat")
print(animal.get_type())

animal2 = AnimalFactory.create_animal("Dog")
print(animal2.get_type())

animal3 = AnimalFactory.create_animal("Parrot")
print(animal3.get_type())
