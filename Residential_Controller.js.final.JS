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
    if((this.queue).length == 0 && this.direction == "idle"){
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
       
    if ((this.selected).length != 0 && (this.queue).length == 0) {
            if (this.direction == "up" && this.floor > Math.max(this.selected)) {
                this.direction = "down";
            } else if (this.direction == "down" && this.floor < Math.min(this.selected)) {
                this.direction = "up";
            }
    }

    if ((this.queue).length == 0 && (this.selected).length == 0) {
        this.direction = "idle";
    }   
        
    };

}

function Controller() {

    this.column = [];
    this.calls = [];

    this.findDirection = function(a, c) {
        if (a.floor > c[0]){
            a.direction = "down";
        } else if (a.floor < c[0]){
            a.direction = "up";
        }
    };

    this.getClosest = function(a, b, c) {
        absA = Math.abs(a.floor - c[0]);
        absB = Math.abs(b.floor - c[0]);
        if (absA > absB) {
            console.log("Elevator B is selected");
            b.queue.push(c[0]);
            index = this.calls.indexOf(c);
            this.calls.splice(index, 1);
                if (b.floor - c[0] > 0) {
                    b.direction = "down";
                } else if (b.floor-c[0] < 0) {
                    b.direction = "up";
            }
        } else if (absB > absA) {
            console.log("Elevator A is selected");
            a.queue.push(c[0]);
            index = this.calls.indexOf(c);
            this.calls.splice(index, 1);
                if (a.floor - c[0] > 0) {
                    a.direction = "down";
                } else if  (a.floor-c[0] < 0) {
                    a.direction = "up";
                }
        } else {
            a.queue.push(c[0]);
            index = this.calls.indexOf(c);
            this.calls.splice(index, 1);
            this.findDirection(a, c);
            console.log("Elevator A is selected");
        }
    };

    this.requestElevator = function(a, b, c) {
        if (a.direction == "idle" && b.direction == "idle") {
            this.getClosest(a, b, c);
        } else if (a.direction != "idle" && b.direction == "idle") {
            if (c[1] == "up") {
                if (a.direction == "up" && c[0] > a.floor) {
                    a.queue.push(c[0]);
                    console.log("Elevator A is selected");
                    index = this.calls.indexOf(c);
                    this.calls.splice(index, 1);
                } else {
                    b.queue.push(c[0]);
                    this.findDirection(b, c);
                    console.log("Elevator B is selected");
                    index = this.calls.indexOf(c);
                    this.calls.splice(index, 1);
                }
            } else{
                if (a.direction == "down" && c[0] < a.floor) {
                    a.queue.push(c[0]);
                    console.log("Elevator A is selected");
                    index = this.calls.indexOf(c);
                    this.calls.splice(index, 1);
                } else {
                    b.queue.push(c[0]);
                    this.findDirection(b, c);
                    console.log("Elevator B is selected");
                    index = this.calls.indexOf(c);
                    this.calls.splice(index, 1);
                }
            }
    
        } else if (b.direction != "idle" && a.direction == "idle") {
            if (c[1] == "up") {
                if (b.direction == "up" && c[0] > b.floor) {
                    b.queue.push(c[0]);
                    console.log("Elevator B is selected");
                    index = this.calls.indexOf(c);
                    this.calls.splice(index, 1);
                } else {
                    a.queue.push(c[0]);
                    this.findDirection(a, c);
                    console.log("Elevator A is selected");
                    index = this.calls.indexOf(c);
                    this.calls.splice(index, 1);
                }
            } else{
                if (b.direction == "down" && c[0] < b.floor) {
                    b.queue.push(c[0]);
                    console.log("Elevator B is selected");
                    index = this.calls.indexOf(c);
                    this.calls.splice(index, 1);
                } else {
                    a.queue.push(c[0]);
                    this.findDirection(a, c);
                    console.log("Elevator A is selected");
                    index = this.calls.indexOf(c);
                    this.calls.splice(index, 1);
                }
            }
    
        } else if (a.direction == "up" && b.direction == "up" && c[1] == "up") {
                if (c[0] > a.floor && c[0] > b.floor) {
                    this.getClosest(a, b, c);
                } else if (c[0] > a.floor) {
                    a.queue.push(c[0]);
                    console.log("Elevator A is selected");
                    index = this.calls.indexOf(c);
                    this.calls.splice(index, 1);
                } else if (c[0] > b.floor) {
                    console.log("Elevator B is selected");
                    b.queue.push(c[0]);
                    index = this.calls.indexOf(c);
                    this.calls.splice(index, 1);
                }
        } else if (a.direction == "down" && b.direction == "down" && c[1] == "down") {
            if (c[0] < a.floor && c[0] < b.floor) {
                this.getClosest(a, b, c);
            } else if (c[0] < a.floor) {
                a.queue.push(c[0]);
                console.log("Elevator A is selected");
                index = this.calls.indexOf(c);
                this.calls.splice(index, 1);
            } else if (c[0] < b.floor) {
                console.log("Elevator B is selected");
                b.queue.push(c[0]);
                index = this.calls.indexOf(c);
                this.calls.splice(index, 1);
            }
        } else if (a.direction != "idle" && b.direction != "idle" && a.direction != b.direction) {
            if (c[1] == "up") {
                if (a.direction == "up" && c[0] > a.floor) {
                    console.log("Elevator A is selected");
                    a.queue.push(c[0]);
                    index = this.calls.indexOf(c);
                    this.calls.splice(index, 1);
                } else if (b.direction == "up" && c[0] > b.floor) {
                    console.log("Elevator B is selected");
                    b.queue.push(c[0]);
                    index = this.calls.indexOf(c);
                    this.calls.splice(index, 1);
                }
            } else{
                if (a.direction == "down" && c[0] < a.floor) {
                    console.log("Elevator A is selected");
                    a.queue.push(c[0]);
                    index = this.calls.indexOf(c);
                    this.calls.splice(index, 1);
                } else if (b.direction == "down" && c[0] < b.floor) {
                    console.log("Elevator B is selected");
                    b.queue.push(c[0]);
                    index = this.calls.indexOf(c);
                    this.calls.splice(index, 1);
                }
            }
        }
    };

    this.selection = function(a, b) {

        var f = prompt("Select the floor you're at:");
        console.log('You are at floor ' + f);
        var d = prompt("Select which direction you are going:");
        console.log('You want to go' + d);
        f = Number(f);
        var c = [f, d];
        this.calls.push(c);
        this.requestElevator(a, b, c);
    };

    this.setup = function(a, b) {
        console.log("We first need to setup the inital configurations");
        i = prompt("First choose Elevator A initial floor:");
        i = Number(i);
        j = prompt("Now select Elevator A initial direction:");
        if (j != "idle") {
            k = prompt("Select Elevator A destination:");
            k = Number(k);
            a.selected.push(k);
        }
        x = prompt("Now select Elevator B initial floor:");
        x = Number(x);
        y = prompt("Select Elevator B initial direction:");
        if (y != "idle") {
           z = prompt("Select Elevator B destination:");
           z = Number(z);
           b.selected.push(z);
        }
        a.floor = i;
        b.floor = x;
        a.direction = j;
        b.direction = y;
        this.selection(a, b);
    };

    this.moveColumn = function(a, b) {

        while ((a.queue).length != 0 || (a.selected).length != 0 || (b.queue).length != 0 || (b.selected).length != 0) {
            for(var i =0; i< (this.column).length; i++){
                if((this.column[i].queue).length == 0 && (this.column[i].selected).length == 0) {
                    this.column[i].direction = "idle";
                }
            }
        
            for(var i = 0; i < (this.column).length; i++) {
                this.column[i].move();
                this.column[i].checkFloor();
            }
        
            for(var i = 0; i < (this.calls).length; i++) {
                this.requestElevator(a, b, this.calls[i]);
            }
        }
    };
    
};

//Setting up the scenarios

controller = new Controller();
elevatorA = new Elevator("A", 2, "idle", "closed");
elevatorB = new Elevator("B", 6, "idle", "closed");
controller.column.push(elevatorA);
controller.column.push(elevatorB);

controller.setup(elevatorA, elevatorB);

while (1 == 1) {

    controller.moveColumn(elevatorA, elevatorB);

    console.log("Both elevators are now empty, waiting for another call");
    controller.selection(elevatorA, elevatorB);
    
}
















