from abc import ABC, abstractmethod

#Zadanie 1.

class Pizza:
  def __init__(self) -> None:
    self.cheese = None
    self.ham = None
    self.salami = None
    self.onion = None
    self.mushroom = None

class PizzaBuilder:
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

class VegetarianPizzaBuilder(PizzaBuilder):
  @abstractmethod
  def add_cheese(self):
    pass
  @abstractmethod
  def add_onion(self):
    pass
  @abstractmethod
  def add_mushroom(self):
    pass

class MeatPizzaBuilder(PizzaBuilder):
  @abstractmethod
  def add_cheese(self):
    pass
  @abstractmethod
  def add_ham(self):
    pass
  @abstractmethod
  def add_salami(self):
    pass

class Director:
  def construct(self, builder):
    builder.add_cheese()
    builder.add_ham()
    builder.add_salami()
    builder.add_onion()
    builder.add_mushroom()
    return builder

vegepizza = VegetarianPizzaBuilder()
director = Director()
pizza = director.construct(vegepizza)

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
