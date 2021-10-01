import abc
from abc import ABC

class Vehicle(ABC):
    def __init__(self, name: str):
        self._name = name

    def who_am_i(self):
        print(f"vehicle: {self._name}  {self}")

class Car(Vehicle):
    def __init__(self, name: str, wheels: int):
        super().__init__(name)
        self._wheels: int = wheels
        print(">> init car")

    def __str__(self):
        return f"{self._name} {self._wheels}"

    def who_am_i(self):
        print(f"car: {self._name}  {self}")

class Boat(Vehicle):
    def __init__(self, name: str, wheels: int):
        super().__init__(name)
        self._motors = wheels
        print(">> init boat")

    def __str__(self):
        return f"{self._name} {self._motors}"

    def who_am_i(self):
        print(f"boat: {self._name}  {self}")        

# example of multiply inheritance
class SwimmingCar(Car, Boat):
    def __init__(self):
        super().__init__("ford", wheels=4)        


vechicle:SwimmingCar = SwimmingCar()
vechicle.who_am_i()
