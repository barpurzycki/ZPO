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
