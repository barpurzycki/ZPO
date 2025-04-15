from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from typing import Any, TextIO
from copy import deepcopy, copy
from time import time
import os
from PIL import Image, ImageOps
import io
import kafka
import pika


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

#Zadanie 3. B

class Scale:
    def scale(self, image: Image.Image, width: int, height: int) -> Image.Image:
        return image.resize((width, height))

class ColorChange:
    def recolor(self, image: Image.Image, color: str) -> Image.Image:
        return ImageOps.grayscale(image)

class Compress:
    def compress(self, image: Image.Image, quality: int) -> io.BytesIO:
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG', quality=quality)
        buffer.seek(0)
        return buffer

class GraphicFacade:
    def __init__(self):
        self.scaler = Scale()
        self.color_changer = ColorChange()
        self.compressor = Compress()

    def image_changer(self, image_path: str, width: int, height: int, color: str, quality: int) -> io.BytesIO:
        image = Image.open(image_path)
        image = self.scaler.scale(image, width, height)
        image = self.color_changer.recolor(image, color)
        return self.compressor.compress(image, quality)

graphic_facade = GraphicFacade()
image_changed = graphic_facade.image_changer("rat.jpeg", 300, 300, "gray", 70)

with open("rat_changed.jpeg", "wb") as f:
    f.write(image_changed.read())

#Zadanie 3. C

class RabbitMQ:
    def __init__(self, host: str = "localhost") -> None:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        channel = self.connection.channel()

    def send_message(self, queue: str, message: str) -> str:
        self.channel.queue_declare(queue=queue)
        self.channel.basic_publish(exchange='', routing_key=queue, body=message)
        print(f'RabbitMQ message: Sent: {message}')

    def receive_message(self, queue: str) -> str:
        self.channel.queue_declare(queue=queue)

        def callback(ch, method, properties, body):
            print(f'RabbitMQ message: Received: {body}')

        self.channel.basic_consume(queue= queue, auto_ack=True, on_message_callback=callback)
        print("Waiting for messages.")
        self.channel.start_consuming()

class Kafka:
    def __init__(self, bootstrap_servers: str ='localhost:9092') -> None:
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
        self.bootstrap_servers = bootstrap_servers

    def send_message(self, topic: str, message: str) -> str:
        self.producer.send(topic, message.encode())
        self.producer.flush()
        print(f'Kafka message: Sent: {message}')

    def receive_message(self, topic: str, callback: str) -> str:
        consumer = KafkaConsumer(topic, bootstrap_servers=self.bootstrap_servers,
                                     auto_offset_reset="earliest", group_id="my-group")
        print(f"Waiting for messages.")
        for msg in consumer:
            callback(msg.value.decode())

class MessageQueueFacade:
    def __init__(self) -> None:
        self.rabbitmq = RabbitMQ()
        self.kafka = Kafka()

    def send_message(self, queue_type: str, destination: str, message: str) -> None:
        if queue_type == "rabbitmq":
            self.rabbitmq.send_message(destination, message)
        elif queue_type == "kafka":
            self.kafka.send_message(destination, message)

    def receive_message(self, queue_type, destination, callback: str) -> None:
        if queue_type == "rabbitmq":
            self.rabbitmq.receive_message(destination)
        elif queue_type == "kafka":
            self.kafka.receive_message(destination, callback)

#Zadanie 4. A

class FileSystemComponent(ABC):
    def __init__(self, item: str) -> None:
        self.item = item

    @abstractmethod
    def display(self, indent: int = 0):
        pass

class File(FileSystemComponent):
    def display(self, indent: int = 0):
        print(' ' * indent + f'|===File: {self.item}')

class Directory(FileSystemComponent):
    def __init__(self, item: str):
        super().__init__(item)
        self.files = []

    def add(self, item: FileSystemComponent):
        self.files.append(item)

    def remove(self, item: FileSystemComponent):
        self.files.remove(item)

    def display(self, indent: int = 0):
        print(' ' * indent + f'Directory: {self.item}')
        for item in self.files:
            item.display(indent + 1)

folder = Directory("folder")
file1 = File("file1.txt")
file2 = File("file2.txt")
subfolder = Directory("subfolder")
file3 = File("file3.txt")

folder.add(file1)
folder.add(subfolder)
subfolder.add(file2)
subfolder.add(file3)

folder.display()
