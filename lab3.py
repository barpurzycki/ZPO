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

#Zadanie 4. B

class Permission:
    def __init__(self, permission : str) -> None:
        self.permission = permission

class PermissionHolder(ABC):
    def __init__(self, name: str):
        self.name = name
        self.permissions = []

    def add_permission(self, permission: Permission) -> None:
        self.permissions.append(permission)

    def remove_permission(self, permission: Permission) -> None:
        self.permissions.remove(permission)

    @abstractmethod
    def has_permission(self, permission: Permission) -> bool:
        pass

class User(PermissionHolder):
    def has_permission(self, permission: Permission) -> bool:
        return permission in self.permissions

class Group(PermissionHolder):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.members = []

    def add_member(self, member:PermissionHolder) -> None:
        self.members.append(member)

    def remove_member(self, member:PermissionHolder) -> None:
        self.members.remove(member)

    def has_permission(self, permission: Permission) -> bool:
        if permission in self.permissions:
            return True
        return any(member.has_permission(permission) for member in self.members)

read = Permission("read")
write = Permission("write")
delete = Permission("delete")

bartek = User("Bartek")
david = User("David")
bartek.add_permission(read)

mods = Group("Moderators")
mods.add_permission(write)
mods.add_member(bartek)

admins = Group("Admins")
admins.add_permission(delete)
admins.add_member(mods)
admins.add_member(david)

# Podgląd
print(f"Bartek permission: 'read': {bartek.has_permission(read)}")
print(f"Bartek permission: 'write': {bartek.has_permission(write)}")
print(f"Bartek permission: 'delete': {bartek.has_permission(delete)}")
print(f"David permission: 'delete': {david.has_permission(delete)}")
print(f"Admins permissions: 'write': {admins.has_permission(write)}")

#Zadanie 4. C

class ReportComponent(ABC):
    @abstractmethod
    def display(self, indent: int = 0) -> None:
        pass

class Value(ReportComponent):
    def __init__(self, name: str, value: float) -> None:
        self.name = name
        self.value = value

    def display(self, indent: int = 0) -> None:
        print(' ' * indent + f'{self.name}: {self.value}')

class ReportSection(ReportComponent):
    def __init__(self, title: str) -> None:
        self.title = title
        self.sections = []

    def add_section(self, section: ReportComponent):
        self.sections.append(section)

    def remove_section(self, section: ReportComponent):
        self.sections.remove(section)

    def display(self, indent: int = 0) -> None:
        print(" " * indent + f"[{self.title}]")
        for section in self.sections:
            section.display(indent + 1)

value1 = Value("value1", 10000)
value2 = Value("value2", 20000)
section1 = ReportSection("Section1")
section1.add_section(value1)
section1.add_section(value2)

other_value1 = Value("Other value1", 30000)
other_value2 = Value("Other value2", 40000)
other_section = ReportSection("Other Section")
other_section.add_section(other_value1)
other_section.add_section(other_value2)

main_report = ReportSection("Report")
main_report.add_section(section1)
main_report.add_section(other_section)
main_report.display()

#Zadanie 5. A

class Document(ABC):
    def __init__(self, text: str) -> None:
        self.text = text

    @abstractmethod
    def get_text(self) -> str:
        pass

    @abstractmethod
    def get_theme(self) -> str:
        pass

class LightTheme(Document):
    text: str

    def get_text(self) -> str:
        return self.text

    def get_theme(self) -> str:
        return "light themed pdf"

class DarkTheme(Document):
    text: str

    def get_text(self) -> str:
        return self.text

    def get_theme(self) -> str:
        return "dark themed pdf"

class PDF(ABC):
    fetcher: Document

    def __init__(self, fetcher: Document) -> None:
        self.fetcher = fetcher

    @abstractmethod
    def show_doc(self) -> str:
        pass

class DarkThemedPDF(PDF):
    fetcher: Document

    def show_doc(self) -> str:
        text = self.fetcher.get_text()

        return f"Theme: Dark, PDF Text: {text}."

class LightThemedPDF(PDF):
    fetcher: Document

    def show_doc(self) -> str:
        text = self.fetcher.get_text()

        return f"Theme: Light, PDF Text: {text}"

text = "Test test test"

fetcher0 = DarkTheme(text)
fetcher1 = LightTheme(text)

light_pdf = LightThemedPDF(fetcher1)
dark_pdf = DarkThemedPDF(fetcher0)

print(light_pdf.show_doc())
print(dark_pdf.show_doc())

#Zadanie 5. B

class Remote(ABC):
    def __init__(self, device_type: str) -> None:
        self.device_type = device_type

    @abstractmethod
    def show_device_type(self):
        pass

class RemoteControl(Remote):
    def show_device_type(self):
        return f"Using {self.device_type.show_device_type()} controller."

class Controller(ABC):
    @abstractmethod
    def show_device_type(self):
        pass

class TVController(Controller):
    def show_device_type(self):
        return "TV"

class RadioController(Controller):
    def show_device_type(self):
        return "Radio"

class DroneController(Controller):
    def show_device_type(self):
        return "Drone"

TV = TVController()
Radio = RadioController()
Drone = DroneController()

tv_controller = RemoteControl(TV)
radio_controller = RemoteControl(Radio)
drone_controller = RemoteControl(Drone)

print(tv_controller.show_device_type())
print(radio_controller.show_device_type())
print(drone_controller.show_device_type())

#Zadanie 5. C

