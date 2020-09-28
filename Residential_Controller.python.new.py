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
        self.status = "on"

    def open(self):
        self.door = door[0]

    def close(self):
        self.door = door[1]
        
    def move(self):
        if self.direction != "idle":
            if self.direction == "up" and self.floor < 10:
                self.floor += 1
            elif self.direction == "down" and self.floor > 1:
                self.floor -= 1
            floor1 = str(self.floor)
            direction1 = self.direction
            print("Elevator " + self.id + " is moving " + direction1 + " and is at floor " + floor1)

    def select(self, n):
        self.queue.append(n)
        if self.direction == "idle":
            if self.floor < n:
                self.direction = "up"
            elif self.floor > n:
                self.direction = "down"

    def selectInElevator(self):
        n = input("Select destination:\n")
        print("You selected floor " + n)
        n = int(n)
        if len(self.queue) == 0:
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
                self.queue.pop()
                self.selectInElevator()

        for item in self.selected:
            if self.floor == item:
                f = str(self.floor)
                print("Elevator " + self.id + " arrived at it's destination")
                self.open()
                print("Doors open")
                print("Waiting for people to get in and out...")
                time.sleep(3)
                print("Doors are now closing")
                self.close()
                self.selected.pop()

        if len(self.queue) == 0 and len(self.selected) == 0:
            self.direction = "idle"
      
class Button:
    def __init__(self, floor, direction):
        self.floor = floor
        self.direction = direction

fl = list(range(11))
door = ['open', 'close']

elevatorA = Elevator("A", 2, "idle", door[1])
elevatorB = Elevator("B", 6, "idle", door[1])
button = Button(fl[0], "idle")

column = [elevatorA, elevatorB]

calledButtons = []

def getClosest(a, b, Button):
    absA = math.fabs(a.floor - Button.floor)
    absB = math.fabs(b.floor - Button.floor)
    if absA > absB:
        b.queue.append(Button.floor)
        calledButtons.pop()
        print("Elevator B is selected")
        if b.floor - button.floor > 0:
            b.direction = "down"
        elif b.floor-Button.floor < 0:
            b.direction = "up"
    elif absB > absA:
        a.queue.append(Button.floor)
        calledButtons.pop()
        print("Elevator A is selected")
        if a.floor - button.floor > 0:
            a.direction = "down"
        elif a.floor-Button.floor < 0:
            a.direction = "up"
    else:
        a.queue.append(Button.floor)
        calledButtons.pop()
        findDirection(a,Button)

def findDirection(a, Button):
    if a.floor > Button.floor:
        a.direction = "down"
    elif a.floor < Button.floor:
        a.direction = "up"

    

def dispatch(Button):
    
    if elevatorA.direction == "idle" and elevatorB.direction == "idle":  #Both are idle
        getClosest(elevatorA, elevatorB, Button)
    elif elevatorA.direction != "idle" and elevatorB.direction == "idle": #A is moving, B is idle
        if Button.direction == "up":
            if elevatorA.direction == "up" and Button.floor > elevatorA.floor:
                elevatorA.queue.append(Button.floor)
                print("Elevator A is selected")
                calledButtons.pop()
            else:
                elevatorB.queue.append(Button.floor)
                print("Elevator B is selected")
                calledButtons.pop()
                findDirection(elevatorB, Button)
        else:
            if elevatorA.direction == "down" and Button.floor < elevatorA.floor:
                elevatorA.queue.append(Button.floor)
                print("Elevator A is selected")
                calledButtons.pop()
            else:
                elevatorB.queue.append(Button.floor)
                print("Elevator B is selected")
                calledButtons.pop()
                findDirection(elevatorB, Button)
    elif elevatorB.direction != "idle" and elevatorA.direction == "idle": #B is moving, A is idle
        if Button.direction == "up":
            if elevatorB.direction == "up" and Button.floor > elevatorB.floor:
                elevatorB.queue.append(Button.floor)
                print("Elevator B is selected ")
                calledButtons.pop()
            else:
                elevatorA.queue.append(Button.floor)
                print("Elevator A is selected")
                calledButtons.pop()
                findDirection(elevatorA, Button)
        else:
            if elevatorB.direction == "down" and Button.floor < elevatorB.floor:
                elevatorB.queue.append(Button.floor)
                print("Elevator B is selected")
                calledButtons.pop()
            else:
                elevatorA.queue.append(Button.floor)
                print("Elevator A is selected")
                calledButtons.pop()
                findDirection(elevatorA, Button)
 
    elif elevatorA.direction == "up" and elevatorB.direction == "up" and Button.direction == "up": #Both are going up and up call
            if Button.floor > elevatorA.floor and Button.floor > elevatorB.floor:
                getClosest(elevatorA, elevatorB, Button)
            elif Button.floor > elevatorA.floor:
                elevatorA.queue.append(Button.floor)
                print("Elevator A is selected")
                calledButtons.pop()
            elif Button.floor > elevatorB.floor:
                elevatorB.queue.append(Button.floor)
                print("Elevator B is selected")
                calledButtons.pop()
    elif elevatorA.direction == "down" and elevatorB.direction == "down" and Button.direction == "down": #Both are going down and down call
        if Button.floor < elevatorA.floor and Button.floor < elevatorB.floor:
            getClosest(elevatorA, elevatorB, Button)
        elif Button.floor < elevatorA.floor:
            elevatorA.queue.append(Button.floor)
            print("Elevator A is selected")
            calledButtons.pop()
        elif Button.floor < elevatorB.floor:
            elevatorB.queue.append(Button.floor)
            print("Elevator B is selected")
            calledButtons.pop()
    elif elevatorA.direction != "idle" and elevatorB.direction != "idle" and elevatorA.direction != elevatorB.direction: #Opposite direction
        if Button.direction == "up":
            if elevatorA.direction == "up" and Button.floor > elevatorA.floor:
                elevatorA.queue.append(Button.floor)
                print("Elevator A is selected")
                calledButtons.pop()
            elif elevatorB.direction == "up" and Button.floor > elevatorB.floor:
                elevatorB.queue.append(Button.floor)
                print("Elevator B is selected")
                calledButtons.pop()
        else:
            if elevatorA.direction == "down" and Button.floor < elevatorA.floor:
                elevatorA.queue.append(Button.floor)
                print("Elevator A is selected")
                calledButtons.pop()
            elif elevatorB.direction == "down" and Button.floor < elevatorB.floor:
                elevatorB.queue.append(Button.floor)
                print("Elevator B is selected")
                calledButtons.pop()

def moveColumn():
    if len(elevatorA.queue) == 0 and len(elevatorA.selected) == 0:
            elevatorA.direction = "idle"
    if len(elevatorB.queue) == 0 and len(elevatorB.selected) == 0:
        elevatorB.direction = "idle"
    for item in column:
        item.move()
        item.checkFloor()
    for item in calledButtons:
        dispatch(item)

    

def selectAtFloor():

    button.floor = input("Select the floor you're at:\n")
    print(f'You are at floor {button.floor}\n')
    button.direction = input("Select which direction you are going:\n")
    print(f'You want to go {button.direction}')
    button.floor = int(button.floor)
        
    calledButtons.append(button)
    dispatch(button)

#Setting up the scenario

def setup():
    print("We first need to setup the inital configurations")
    i = input("First choose Elevator A initial floor:\n")
    i = int(i)
    j = input("Now select Elevator A initial direction:\n")
    if j != "idle":
        k = input("Select Elevator A destination: \n")
        k = int(k)
        elevatorA.selected.append(k)
    x = input("Now select Elevator B initial floor: \n")
    x = int(x)
    y = input("Select Elevator B initial direction:\n")
    if y != "idle":
        z = input("Select Elevator B destination:\n")
        z = int(z)
        elevatorB.selected.append(z)
    elevatorA.floor = i
    elevatorB.floor = x
    elevatorA.direction = j
    elevatorB.direction = y
    selectAtFloor()

setup()

while True:
    while len(elevatorA.queue) != 0 or len(elevatorA.selected) != 0 or len(elevatorB.queue) != 0 or len(elevatorB.selected) != 0 :
        moveColumn()
        time.sleep(1)

    if len(elevatorA.queue) == 0 and len(elevatorA.selected) == 0 and len(elevatorB.queue) == 0 and len(elevatorB.selected) == 0:

        print("Both elevators are now empty, waiting for another call")
        selectAtFloor()




  














