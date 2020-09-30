# Define Objects
import time 
import math

class Elevator:
    def __init__(self, id, floor, direction, door ):
        self.id = id
        self.floor = floor
        self.direction = direction
        self.door = door
        self.queue = []
        self.selected = []

    def open(self):
        self.door = "open"

    def close(self):
        self.door = "closed"
        
    def move(self):
        if self.direction != "idle":
            if self.direction == "up" and self.floor < 10:
                self.floor += 1
            elif self.direction == "down" and self.floor > 1:
                self.floor -= 1
            floor1 = str(self.floor)
            direction1 = self.direction
            print("Elevator " + self.id + " is moving " + direction1 + " and is at floor " + floor1)

    def requestFloor(self):
        n = input("Select destination:\n")
        print("You selected floor " + n)
        n = int(n)
        if len(self.queue) == 0 and self.direction == "idle":
            if self.floor > n:
                self.direction = "down"
            elif self.floor < n:
                self.direction = "up"
        self.selected.append(n)

    def checkFloor(self):
        for item in self.queue:
            if self.floor == item:
                f = str(self.floor)
                print("Elevator " + self.id + " arrived at floor " + f)
                self.open()
                print("Doors open")
                print("Waiting for people to get in and out...")
                time.sleep(5)
                print("Doors are now closing")
                self.close()
                self.queue[:] = [x for x in self.queue if x != item]
                self.requestFloor()
        
        for item in self.selected:
            if self.floor == item:
                print("Elevator " + self.id + " arrived at it's destination")
                self.open()
                print("Doors open")
                print("Waiting for people to get in and out...")
                time.sleep(3)
                print("Doors are now closing")
                self.close()
                self.selected[:] = [x for x in self.selected if x != item]

        if len(self.selected) != 0 and len(self.queue) == 0:
            if self.direction == "up" and self.floor > max(self.selected):
                self.direction = "down"
            elif self.direction == "down" and self.floor < min(self.selected):
                self.direction = "up"

        if len(self.queue) == 0 and len(self.selected) == 0:
            self.direction = "idle"
      
class Controller:
    def __init__(self):
        self.column = []
        self.calls = []
        
    
    def findDirection(self, a, c):
        if a.floor > c[0]:
            a.direction = "down"
        elif a.floor < c[0]:
            a.direction = "up"
    
    def getClosest(self, a, b, c):
        absA = math.fabs(a.floor - c[0])
        absB = math.fabs(b.floor - c[0])
        if absA > absB:
            b.queue.append(c[0])
            self.calls.remove(c)
            print("Elevator B is selected")
            if b.floor - c[0] > 0:
                b.direction = "down"
            elif b.floor-c[0] < 0:
                b.direction = "up"
        elif absB > absA:
            a.queue.append(c[0])
            self.calls.remove(c)
            print("Elevator A is selected")
            if a.floor - c[0] > 0:
                a.direction = "down"
            elif a.floor - c[0] < 0:
                a.direction = "up"
        else:
            a.queue.append(c[0])
            self.calls.remove(c)
            self.findDirection(a, c)
            print("Elevator A is selected")

    def requestElevator(self, a, b, c): 
    
        if a.direction == "idle" and b.direction == "idle":  #Both are idle
            self.getClosest(a, b, c)
        elif a.direction != "idle" and b.direction == "idle": #A is moving, B is idle
            if c[1] == "up":
                if a.direction == "up" and c[0] > a.floor:
                    a.queue.append(c[0])
                    print("Elevator A is selected")
                    self.calls.remove(c)
                else:
                    b.queue.append(c[0])
                    print("Elevator B is selected")
                    self.calls.remove(c)
                    self.findDirection(b, c)
            else:
                if a.direction == "down" and c[0] < a.floor:
                    a.queue.append(c[0])
                    print("Elevator A is selected")
                    self.calls.remove(c)
                else:
                    b.queue.append(c[0])
                    print("Elevator B is selected")
                    self.calls.remove(c)
                    self.findDirection(b, c)
        elif b.direction != "idle" and a.direction == "idle": #B is moving, A is idle
            if c[1] == "up":
                if b.direction == "up" and c[0] > b.floor:
                    b.queue.append(c[0])
                    print("Elevator B is selected ")
                    self.calls.remove(c)
                else:
                    a.queue.append(c[0])
                    print("Elevator A is selected")
                    self.calls.remove(c)
                    self.findDirection(a, c)
            else:
                if b.direction == "down" and c[0] < b.floor:
                    b.queue.append(c[0])
                    print("Elevator B is selected")
                    self.calls.remove(c)
                else:
                    a.queue.append(c[0])
                    print("Elevator A is selected")
                    self.calls.remove(c)
                    self.findDirection(a, c)
    
        elif a.direction == "up" and b.direction == "up" and c[1] == "up": #Both are going up and up call
                if c[0] > a.floor and c[0] > b.floor:
                    self.getClosest(a, b, c)
                elif c[0] > a.floor:
                    a.queue.append(c[0])
                    print("Elevator A is selected")
                    self.calls.remove(c)
                elif c[0] > b.floor:
                    b.queue.append(c[0])
                    print("Elevator B is selected")
                    self.calls.remove(c)
        elif a.direction == "down" and b.direction == "down" and c[1] == "down": #Both are going down and down call
            if c[0] < a.floor and c[0] < b.floor:
                self.getClosest(a, b, c)
            elif c[0] < a.floor:
                a.queue.append(c[0])
                print("Elevator A is selected")
                self.calls.remove(c)
            elif c[0] < b.floor:
                b.queue.append(c[0])
                print("Elevator B is selected")
                self.calls.remove(c)
        elif a.direction != "idle" and b.direction != "idle" and a.direction != b.direction: #Opposite direction
            if c[1] == "up":
                if a.direction == "up" and c[0] > a.floor:
                    a.queue.append(c[0])
                    print("Elevator A is selected")
                    self.calls.remove(c)
                elif b.direction == "up" and c[0] > b.floor:
                    b.queue.append(c[0])
                    print("Elevator B is selected")
                    self.calls.remove(c)
            else:
                if a.direction == "down" and c[0] < a.floor:
                    a.queue.append(c[0])
                    print("Elevator A is selected")
                    self.calls.remove(c)
                elif b.direction == "down" and c[0] < b.floor:
                    b.queue.append(c[0])
                    print("Elevator B is selected")
                    self.calls.remove(c)

    def selection(self, a, b):

        f = input("Select the floor you're at:\n")
        print(f'You are at floor {f}\n')
        d = input("Select which direction you are going:\n")
        print(f'You want to go {d}\n')
        f = int(f)
        c = [f, d]
        self.calls.append(c)
        self.requestElevator(a, b, c)

    def setup(self, a, b):
        print("We first need to setup the inital configurations")
        i = input("First choose Elevator A initial floor:\n")
        i = int(i)
        j = input("Now select Elevator A initial direction:\n")
        if j != "idle":
            k = input("Select Elevator A destination: \n")
            k = int(k)
            a.selected.append(k)
        x = input("Now select Elevator B initial floor: \n")
        x = int(x)
        y = input("Select Elevator B initial direction:\n")
        if y != "idle":
            z = input("Select Elevator B destination:\n")
            z = int(z)
            b.selected.append(z)
        a.floor = i
        b.floor = x
        a.direction = j
        b.direction = y
        self.selection(a, b)

    def moveColumn(self, a, b):
        while len(a.queue) != 0 or len(a.selected) != 0 or len(b.queue) != 0 or len(b.selected) != 0 :
            for item in self.column:
                if len(item.queue) == 0 and len(item.selected) == 0:
                        item.direction = "idle"
            for item in self.column:
                item.move()
                item.checkFloor()
            for item in self.calls:
                self.requestElevator(a, b, item)
            time.sleep(1)

#Setting up the scenarios

controller = Controller()
elevatorA = Elevator("A", 2, "idle", "closed")
elevatorB = Elevator("B", 6, "idle", "closed")
controller.column.append(elevatorA)
controller.column.append(elevatorB)

controller.setup(elevatorA, elevatorB)

while True:
    
    controller.moveColumn(elevatorA, elevatorB)

    print("Both elevators are now empty, waiting for another call")
    controller.selection(elevatorA, elevatorB)




  














