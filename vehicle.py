
class Vehicle:
    def __init__(self, price, color):
        self.color = color
        self.price = price
        self.gas = 0

    def fillUpTank(self):
        self.gas = 100

    def emptyTank(self):
        self.gas = 0

    def gasLeft(self):
        return self.gas


class Truck(Vehicle):
    def __init__(self, price, color, tires):
        super().__init__(price, color)
        self.tires = tires

    def beep(self):
        print("Honk honk")


class Car(Vehicle):
    def __init__(self, price, color, speed):
        super().__init__(price, color)
        self.speed = speed

    def beep(self):
        print("Beep Beep")

    def changeColor(self, newColor):
        self.color = newColor
        print("Changed color to :", self.color)


smallVehicle = Car(100, "red", 10)
smallVehicle.beep()
smallVehicle.changeColor("white")

bigVehicle = Truck(250, "yellow", 4)
bigVehicle.beep()
