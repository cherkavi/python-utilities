class Vehicle:
    def who_am_i(self):
        print("vehicle: ", self)

class Car(Vehicle):
    def who_am_i(self):
        print("car: ", self)

class Boat(Vehicle):
    def who_am_i(self):
        print("boat: ", self)

# example of multiply inheritance
class SwimmingCar(Car, Boat):
    pass


vechicle: (Boat, Car) = SwimmingCar()
vechicle.who_am_i()
