# Define Objects

#Note that sometimes this python file doesn't work on VS code terminal "Run python on terminal"
#The rest function is there, but I couldn't get it to run properly/////
#From what I gathered on the intertrons, this might be a problem with VS code. Thank you.

import time 
import math
import threading

class Elevator:
    def __init__(self, id, floor, direction, door, restFloor ):
        self.id = id
        self.floor = floor  #integer
        self.direction = direction # idle/down/up
        self.door = door
        self.queue = []
        self.selected = []
        self.capacity = 0
        self.restFloor = restFloor

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
            if self.floor == item:      #Check if someone is at destionation
                f = str(self.floor)
                print("Elevator " + self.id + " arrived at floor " + f)
                self.open()
                print("Doors open")
                x = str(self.capacity)         #Check the weight requirement of the elevator
                print("There is " + x + " person inside \n" )
                z = input("How many persons are getting in? \n")
                z = int(z)
                while self.capacity + z > 15 or z < 0:
                    print("Elevator is empty or have 15 persons maximum! \n")
                    z = input("How many persons are lucky enough to get in? \n")
                    z = int(z)
                self.capacity += z
                a = str(self.capacity)
                print("Waiting for people to get in ...")
                time.sleep(3)
                print("There is now " + a + " person inside \n")
                print("Doors are now closing")
                self.close()
                self.queue[:] = [x for x in self.queue if x != item]
                self.requestFloor()
        
        for item in self.selected:
            if self.floor == item:     #Check if someone made a call on this floor
                print("Elevator " + self.id + " arrived at it's destination")
                self.open()
                print("Doors open")

                x1 = str(self.capacity)     #Weight requirement
                print("There is " + x1 + " person inside \n" )
                y1 = input("How many persons are getting out? \n")
                y1 = int(y1)

                while y1 > self.capacity or y1 < 0:
                    print("Elevator is empty or have 15 persons maximum! \n")
                    y1 = input("How many persons are getting out? \n")
                    y1 = int(y1)
                    
                self.capacity -= y1
                a1 = str(self.capacity)
                print("Waiting for people to get out...")
                time.sleep(3)
                print("There is now " + a1 + " person inside \n")
                print("Doors are now closing")

                self.close()
                self.selected[:] = [x for x in self.selected if x != item]

        if len(self.selected) != 0 and len(self.queue) == 0:     #Change direction if unanswered calls are in opposite direction
            if self.direction == "up" and self.floor > max(self.selected):
                self.direction = "down"
            elif self.direction == "down" and self.floor < min(self.selected):
                self.direction = "up"

        if len(self.queue) == 0 and len(self.selected) == 0:  #Set rest floor after some time
            self.direction = "idle"                        
            #if self.floor != self.restFloor and self.capacity == 0:
                #threading.Timer(10, self.rest())
            if self.capacity != 0:                              # Check for people still in elevator
                print("Elevator " + self.id + " has no more calls, but there's still people inside!")
                print("Where do they wanna go?")
                self.requestFloor()

    def rest(self):     #Elevator go to rest floor
        self.queue.append(self.restFloor)
        x = str(self.restFloor)
        print("Elevator " + self.id + " go back to rest floor " + x)
        if self.floor > self.restFloor:
            self.direction = "down"
        else :
            self.direction = "up"
                
            
         
      
class Controller:
    def __init__(self):
        self.column = []
        self.calls = []
        
    
    def findDirection(self, a, c):
        if a.floor > c[0]:
            a.direction = "down"
        elif a.floor < c[0]:
            a.direction = "up"
    
    def getClosest(self, a, b, c):    #Find closest elevator to call
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

    def selection(self, a, b):    #Initial selection

        f = input("Select the floor you're at:\n")
        print(f'You are at floor {f}\n')
        d = input("Select which direction you are going:\n")
        print(f'You want to go {d}\n')
        f = int(f)
        c = [f, d]
        self.calls.append(c)
        self.requestElevator(a, b, c)

    def setup(self, a, b):   #Setup the initial configurations for scenarios
        c = [a, b]
        print("We first need to setup the inital configurations")
        for i in c:
            i.floor = input("First choose Elevator " + i.id +  " initial floor:\n")
            i.floor = int(i.floor)
            i.direction = input("Now select Elevator " + i.id + " initial direction:\n")
            if i.direction != "idle":
                k = input("Select Elevator " + i.id + " destination: \n")
                k = int(k)
                i.selected.append(k)
                i.capacity = input("How many persons are in the elevator? \n")
                i.capacity = int(i.capacity)
                while i.capacity > 15 or i.capacity < 0 :
                    print("Elevator is empty or with 15 persons maximum!")
                    i.capacity = input("How many persons are in the elevator? \n")
                    i.capacity = int(i.capacity)
        self.selection(a, b)

    def moveColumn(self, a, b):   #Make everything move
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
elevatorA = Elevator("A", 2, "idle", "closed", 1)
elevatorB = Elevator("B", 6, "idle", "closed", 5)
controller.column.append(elevatorA)
controller.column.append(elevatorB)

controller.setup(elevatorA, elevatorB)

while True:
    
    controller.moveColumn(elevatorA, elevatorB)

    print("Both elevators are now empty, waiting for another call")
    controller.selection(elevatorA, elevatorB)




  














