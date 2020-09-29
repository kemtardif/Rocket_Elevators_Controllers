const prompt = require('prompt-sync')();

//////TO RUN THE SCENARIOS, USE NODE WITH THE EXTENSION prompt-sync THANK YOU////////
// Define Objects

function Elevator (id, floor, direction, door){
    
    this.id = id
    this.floor = floor;
    this.direction = direction;
    this.door = door;
    this.queue = [];
    this.selected = [];

    this.open = function() {
        this.door = door[0];
    };

    this.close = function() {
        this.door = door[1];
    };

    this.move = function() {
        
        if (this.direction != "idle") {
            if (this.direction == "up" && this.floor < 10) {
                this.floor += 1;
            } else if (this.direction == "down" && this.floor > 1) {
                this.floor -= 1;
            }
        }
        
        floor1 = (this.floor).toString();
        direction1 = this.direction;
        console.log("Elevator " + this.id + " is " + direction1 + " and is at floor " + floor1);
    };
   
    this.requestFloor = function() {
    n = prompt("Select destination: ");
    if((this.queue).length == 0){
        if (this.floor < n) {
            this.direction = "up";
        } else if (this.floor > n) {
             this.direction = "down";
        }
    }
        this.selected.push(n);
    };

    this.checkFloor = function() {

    for( var x = 0; x < (this.queue).length; x++) {
        if (this.floor == this.queue[x]) {
            f = (this.floor).toString();
            console.log("Elevator " + this.id + " arrived at floor " + f);
            this.open(); 
            console.log("Doors open");
            console.log("Waiting for people to get in and out...");  
            //Sleep for 5 seconds
            console.log("Doors are closing");
            this.close();
            this.queue.splice(x, 1);
            this.requestFloor();
         }
     }

    for (var x = 0; x < (this.selected).length; x++){
        if (this.floor == this.selected[x]) {
            console.log("Elevator " + this.id + " arrived at it's destination");
            this.open();
            console.log("Doors open");
            console.log("Waiting for people to get in and get out...");
            //Sleep for 5 seconds
            console.log("Doors are now closing");
            this.close();
            this.selected.splice(x, 1);
        }
    }
       
    if ((this.queue).length == 0 && (this.selected).length == 0) {
        this.direction = "idle";

    }   
        
    };

}

function Button(floor, direction) {
    this.floor = floor;
    this.direction = direction;

    this.findDirection = function(a) {
        if (a.floor > this.floor){
            a.direction = "down";
        } else if (a.floor < this.floor){
            a.direction = "up";
        }
    };

    this.getClosest = function(a, b) {
        absA = Math.abs(a.floor - this.floor);
        absB = Math.abs(b.floor - this.floor);
        if (absA > absB) {
            console.log("Elevator B is selected");
            b.queue.push(this.floor);
            calledButtons.pop();
                if (b.floor - this.floor > 0) {
                    b.direction = "down";
                } else if (b.floor-this.floor < 0) {
                    b.direction = "up";
            }
        } else if (absB > absA) {
            console.log("Elevator A is selected");
            a.queue.push(this.floor);
            calledButtons.pop();
                if (a.floor - this.floor > 0) {
                    a.direction = "down";
                } else if  (a.floor-this.floor < 0) {
                    a.direction = "up";
                }
        } else {
            a.queue.push(this.floor);
            calledButtons.pop();
            this.findDirection(a);
            console.log("Elevator A is selected");
        }
    };

    this.requestElevator = function() {
        if (elevatorA.direction == "idle" && elevatorB.direction == "idle") {
            this.getClosest(elevatorA, elevatorB);
        } else if (elevatorA.direction != "idle" && elevatorB.direction == "idle") {
            if (this.direction == "up") {
                if (elevatorA.direction == "up" && this.floor > elevatorA.floor) {
                    elevatorA.queue.push(this.floor);
                    console.log("Elevator A is selected");
                    calledButtons.pop();
                } else {
                    elevatorB.queue.push(this.floor);
                    this.findDirection(elevatorB);
                    console.log("Elevator B is selected");
                    calledButtons.pop();
                }
            } else{
                if (elevatorA.direction == "down" && this.floor < elevatorA.floor) {
                    elevatorA.queue.push(this.floor);
                    console.log("Elevator A is selected");
                    calledButtons.pop();
                } else {
                    elevatorB.queue.push(this.floor);
                    this.findDirection(elevatorB);
                    console.log("Elevator B is selected");
                    calledButtons.pop();
                }
            }
    
        } else if (elevatorB.direction != "idle" && elevatorA.direction == "idle") {
            if (this.direction == "up") {
                if (elevatorB.direction == "up" && this.floor > elevatorB.floor) {
                    elevatorB.queue.push(this.floor);
                    console.log("Elevator B is selected");
                    calledButtons.pop();
                } else {
                    elevatorA.queue.push(this.floor);
                    this.findDirection(elevatorA);
                    console.log("Elevator A is selected");
                    calledButtons.pop();
                }
            } else{
                if (elevatorB.direction == "down" && this.floor < elevatorB.floor) {
                    elevatorB.queue.push(this.floor);
                    console.log("Elevator B is selected");
                    calledButtons.pop();
                } else {
                    elevatorA.queue.push(this.floor);
                    this.findDirection(elevatorA);
                    console.log("Elevator A is selected");
                    calledButtons.pop();
                }
            }
    
        } else if (elevatorA.direction == "up" && elevatorB.direction == "up" && this.direction == "up") {
                if (this.floor > elevatorA.floor && this.floor > elevatorB.floor) {
                    this.getClosest(elevatorA, elevatorB);
                } else if (this.floor > elevatorA.floor) {
                    elevatorA.queue.push(this.floor);
                    console.log("Elevator A is selected");
                    calledButtons.pop();
                } else if (this.floor > elevatorB.floor) {
                    console.log("Elevator B is selected");
                    elevatorB.queue.push(this.floor);
                    calledButtons.pop();
                }
        } else if (elevatorA.direction == "down" && elevatorB.direction == "down" && this.direction == "down") {
            if (this.floor < elevatorA.floor && this.floor < elevatorB.floor) {
                this.getClosest(elevatorA, elevatorB);
            } else if (this.floor < elevatorA.floor) {
                elevatorA.queue.push(this.floor);
                console.log("Elevator A is selected");
                calledButtons.pop();
            } else if (this.floor < elevatorB.floor) {
                console.log("Elevator B is selected");
                elevatorB.queue.push(this.floor);
                calledButtons.pop();
            }
        } else if (elevatorA.direction != "idle" && elevatorB.direction != "idle" && elevatorA.direction != elevatorB.direction) {
            if (this.direction == "up") {
                if (elevatorA.direction == "up" && this.floor > elevatorA.floor) {
                    console.log("Elevator A is selected");
                    elevatorA.queue.push(this.floor);
                    calledButtons.pop();
                } else if (elevatorB.direction == "up" && this.floor > elevatorB.floor) {
                    console.log("Elevator B is selected");
                    elevatorB.queue.push(this.floor);
                    calledButtons.pop();
                }
            } else{
                if (elevatorA.direction == "down" && this.floor < elevatorA.floor) {
                    console.log("Elevator A is selected");
                    elevatorA.queue.push(this.floor);
                    calledButtons.pop();
                } else if (elevatorB.direction == "down" && this.floor < elevatorB.floor) {
                    console.log("Elevator B is selected");
                    elevatorB.queue.push(this.floor);
                    calledButtons.pop();
                }
            }
        }
    };

    this.selectAtFloor = function() {

        this.floor = prompt("Select the floor you're at:");
        console.log('You are at floor ' + this.floor);
        this.direction = prompt("Select which direction you are going:");
        console.log('You want to go' + this.direction);
        this.floor = Number(this.floor);
            
        calledButtons.push(this);
        this.requestElevator();
    };
};

var door = ['open', 'close'];
var door = ['open', 'close'];
var calledButtons = [];

elevatorA = new Elevator("A", 2, "idle", door[1]);
elevatorB = new Elevator("B", 6, "idle", door[1]);
button = new Button(1, "idle")
var column = [elevatorA, elevatorB];
    
function moveColumn() {

    for(var i =0; i< (column).length; i++){
        if((column[i].queue).length == 0 && (column[i].selected).length == 0) {
            column[i].direction = "idle";
        }
    }

    for(var i = 0; i < (column).length; i++) {
        column[i].move();
        column[i].checkFloor();
    }

    for(var i = 0; i < (calledButtons).length; i++) {
        calledButtons[i].requestElevator();
    }
};

//Setting up the scenario

function setup() {
    console.log("We first need to setup the inital configurations");
    i = prompt("First choose Elevator A initial floor:");
    i = Number(i);
    j = prompt("Now select Elevator A initial direction:");
    if (j != "idle") {
        k = prompt("Select Elevator A destination:");
        k = Number(k);
        elevatorA.selected.push(k);
    }
    x = prompt("Now select Elevator B initial floor:");
    x = Number(x);
    y = prompt("Select Elevator B initial direction:");
    if (y != "idle") {
       z = prompt("Select Elevator B destination:");
       z = Number(z);
       elevatorB.selected.push(z);
    }
    elevatorA.floor = i;
    elevatorB.floor = x;
    elevatorA.direction = j;
    elevatorB.direction = y;
    button.selectAtFloor();
};

setup();

while (1 == 1) {
    while ((elevatorA.queue).length != 0 || (elevatorA.selected).length != 0 || (elevatorB.queue).length != 0 || (elevatorB.selected).length != 0) {
        moveColumn()
        //time.sleep(1)
    }

    if ((elevatorA.queue).length == 0 && (elevatorA.selected).length == 0 && (elevatorB.queue).length == 0 && (elevatorB.selected).length == 0) {

        console.log("Both elevators are now empty, waiting for another call");
        button.selectAtFloor()
    }
}
















