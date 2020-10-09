using System;
using System.Linq;
using System.Collections.Generic;

namespace Commercial_Controller
{
    class Program
    {
        static void Main(string[] args)
        {
            Controller controller = new Controller(60, 6, 4, 5);  // # of non-basement floors, # of basements, # of columns, elev/columns

            Console.WriteLine("Choose which floor you're at (Negative for basements and RC is 1)");
            int n = Convert.ToInt32(Console.ReadLine());

            if (n == 1) {
                controller.assignElevator();
            } else {
                 controller.requestElevator(n);
            }

            while (1 == 1)  {
                foreach (Elevator item in controller.elevators){
                    item.checkFloor();
                    item.move();
                }
            }

        }
    }

    class Controller {
        public int selectedColumn; //column selected for call. -1 for basements, 1 first column, 2 for the one above, etc.
        public static int deserving; //# of floors deserved by each upper columns. Basement column deserve all basements.
        public static int basements;  //# of basements
        public static int totalColumns; 
        public static int upperFloor;  //top floor

        public List<Elevator> elevators = new List<Elevator>(){};

        public Controller(int upper, int bases, int columns, int elevPerColumns ) {

            for (int i = 0; i < elevPerColumns; i++){ 

                elevators.Add( new Elevator());
            }

            deserving = (upper-(upper%(columns-1)))/(columns - 1); //Upper columns serve same # of floors, except top column taking care of the remainder
            basements = bases;
            totalColumns = columns;
            upperFloor = upper;
        }

        public void requestElevator(int n) {

            selection(n);
            initialize();

            if (n < 0) {
                requestBelow(n);
            } else {
                requestAbove(n);
            }
        }

        public void selection(int n) {  //Select appropriate column

            if ( n >= -(basements-1) && n < 1){  //Basements

                selectedColumn = 0;
                char selected = (char)(65);
            
            Console.WriteLine("Column " + selected + " is selected");
            Console.WriteLine("This column deserves " + basements + " basements");

            }else if( n > deserving*(totalColumns - 2) && n <= upperFloor){  //Top column

                selectedColumn = totalColumns - 1;
                char selected = (char)(selectedColumn + 65);

                int x = deserving*(totalColumns - 2) + 1; //Convert integer to letter
                Console.WriteLine("Column " + selected + " is selected");
                Console.WriteLine("This column deserves floor " + x + " up to " + upperFloor);

            }else {
                
                for ( int i = 0; i < totalColumns - 2; i++){ // Other upper columns

                    if( n > deserving*i && n <= deserving*(i + 1)){
                        selectedColumn = i + 1;
                        char selected = (char)(selectedColumn + 65);

                        int x = deserving*i + 1;
                        int y = deserving*(i+1);
                        Console.WriteLine("Column " + selected + " is selected");
                        Console.WriteLine("This column deserves floor " + x + " up to " + y);
                    }
                }
            }

        }

        public void initialize () {

            for (int i = 0; i < elevators.Count(); i++){

                int a = i + 1;
                Console.WriteLine("Elevator " + a + " status is (idle/up/down):");
                string s1 = Console.ReadLine();
                Console.WriteLine("Elevator " + a + " current floor is:");
                int f1 = Convert.ToInt32(Console.ReadLine());
                int d1 = 0;

                if ( s1 != "idle" ) {

                    Console.WriteLine("Elevator " + a + " destination is: ");
                        d1 = Convert.ToInt32(Console.ReadLine());

                        if (d1 == 1){
                            elevators[i].selected = true; //Condition to go to RC

                        } else if( d1 < f1 && s1 == "down" && d1 > 0) {
                            elevators[i].selected = true;
                            elevators[i].queue.Add(d1);

                        }else if (d1 > f1 && s1 == "up" && d1 < 0){
                            elevators[i].selected = true;
                            elevators[i].queue.Add(d1);

                        }else {
                            elevators[i].selected = false;
                            elevators[i].queue.Add(d1);
                        }

                    Console.WriteLine("How many persons are in this elevator?");
                    int z  = Convert.ToInt32(Console.ReadLine());

                    while ( z > 15 || z < 0){

                        Console.WriteLine("Elevator is empty or have 15 persons maximum!");
                        Console.WriteLine("How many persons are in this elevator?");

                        z = Convert.ToInt32(Console.ReadLine());
                    }
                    elevators[i].capacity = z;

                } else {
                    elevators[i].capacity = 0;
                }

                elevators[i].id = a;
                elevators[i].status = s1;
                elevators[i].currentFloor = f1;
                elevators[i].destination = 0;
            }
        }

        public void requestAbove(int n) {  //Select elevator for a call made on a floor

            List<int> ups = new List<int>();
            List<int> idles = new List<int>();


            foreach (Elevator item in elevators) {    

                if (item.currentFloor >= n && item.status == "down"){  //Above and going down first
                    ups.Add(item.currentFloor);
                } else if (item.status == "idle"){    //Idle second
                    idles.Add(item.currentFloor);
                }
             }
        
             if (ups.Count() != 0) {   //Line 128 to 149 select closest if more than one elevators satisy the above

                int up = getClosest(n, ups);

                foreach (Elevator item in elevators) {

                    if(item.currentFloor >= n && item.status == "down" && item.currentFloor == up){
                        Console.WriteLine("Elevator " + item.id + " is selected. Press enter.");
                        Console.ReadLine();

                        item.selected = true;
                        item.queue.Add(n);
                        item.selectDirection(n);
                        return;
                    } 
                }
             } else if (idles.Count() != 0){

                int idle = getClosest(n, idles);

                foreach (Elevator item in elevators) {

                    if ( item.status == "idle" && item.currentFloor == idle) {
                        Console.WriteLine("Elevator " + item.id + " is selected. Press enter.");
                        Console.ReadLine();

                        item.selected = true;
                        item.queue.Add(n);
                        item.selectDirection(n);
                        return;
                    } 
                 }

             }
            return;
        }

        

        public void requestBelow(int n) {  //Same logic, but for basements

            List<int> downs = new List<int>();
            List<int> idles = new List<int>();

            foreach (Elevator item in elevators) {

                if (item.currentFloor <= n && item.status == "up"){
                    downs.Add(item.currentFloor);
                } else if (item.status == "idle"){
                    idles.Add(item.currentFloor);
                }
             }
            
             if (downs.Count() != 0){

                int down = getClosest(n, downs);

                foreach (Elevator item in elevators) {

                    if(item.currentFloor <= n && item.status == "up" && item.currentFloor == down){
                        Console.WriteLine("Elevator " + item.id + " is selected. Press enter.");
                        Console.ReadLine();

                        item.selected = true;
                        item.queue.Add(n);
                        item.selectDirection(n);
                        return;
                    } 
                }
            } else if (idles.Count() != 0){

                int idle = getClosest(n, idles);

                foreach (Elevator item in elevators) {

                    if ( item.status == "idle" && item.currentFloor == idle) {
                        Console.WriteLine("Elevator " + item.id + " is selected. Press enter.");
                        Console.ReadLine();

                        item.selected = true;
                        item.queue.Add(n);
                        item.selectDirection(n);
                        return;
                    } 
                }
            }

            return;
        }

        public int getClosest(int n, List<int> ls) {   //Select closest elevator to call at floor n

            List<int> minDistance = new List<int>();

            for (int i = 0; i < ls.Count(); i++) {
                minDistance.Add(Math.Abs(n - ls[i]));
            }
            int min = ls.Min();

            for (int i = 0; i < ls.Count(); i++ ){
                if (minDistance[i] == min){
                    return ls[i];
                }
            }
            return min;
        }

        public void assignElevator() {   //Select appropriate elevator for call made at RC

            Console.WriteLine("Select which floor you want to go to (Negative integers for basements, Rc is 1 and 0 is not a floor)");
            int n = Convert.ToInt32(Console.ReadLine());

            selection(n);
            initialize();

            if (n < 0) {
                lowerRC(n);
            } else {
                upperRC(n);
            }


        }

        public void upperRC(int n) {

            List<int> ups = new List<int>();
            List<int> idles = new List<int>();

            foreach (Elevator item in elevators) {      

                if (item.currentFloor == 1 && item.status == "up"){   //Select elevator at RC going up first
                    ups.Add(item.destination);
                } else if (item.currentFloor == 1 && item.status == "idle"){ //At RC and idle second
                    idles.Add(item.id);
                }
             }

             if (ups.Count() != 0 ) {  //Again, line 267 to 294 select closest in case more than one satisfy the above

             int up = getClosest(n, ups);
             
             foreach (Elevator item in elevators) {

                 if(item.currentFloor == 1 && item.status == "up" && item.destination == up){
                    Console.WriteLine("Elevator " + item.id + " is selected. Press enter.");
                    Console.ReadLine();

                    item.selected = true;
                    item.destination = n;
                    return;
                 } 
             }
             } else if (idles.Count() != 0) {

                    Console.WriteLine("Elevator " + idles[0] + " is selected. Press enter.");
                    Console.ReadLine();

                    elevators[idles[0] -1].selected = true;
                    elevators[idles[0] -1].destination = n;
                    return;
            } else { 

                List<int> downs = new List<int>();

                foreach (Elevator item in elevators){

                    if (item.status == "down") {
                     downs.Add(item.currentFloor);
                    }
                }

                if (downs.Count() != 0) {
                    int down = getClosest(1, downs);
                
                    foreach (Elevator item in elevators) {

                        if (item.currentFloor == down && item.status == "down") {
                            Console.WriteLine("Elevator " + item.id + " is selected. Press enter.");
                            Console.ReadLine();

                            
                            item.selected = true;
                            item.destination = n;
                            return;
                        }
                    }
                } else {

                    List<int> others = new List<int>();

                    foreach(Elevator item in elevators) {
                        others.Add(item.currentFloor);
                    }

                    int other = getClosest(n, others);
                
                    foreach (Elevator item in elevators) {

                        if (item.currentFloor == other) {

                            Console.WriteLine("Elevator " + item.id + " is selected. Press enter.");
                            Console.ReadLine();

                            item.selected = true;
                            item.destination = n;
                            return;
                        }
                    }
                }
            }
        }

        public void lowerRC(int n) {  //Same logic, but for basements

            List<int> downs = new List<int>();
            List<int> idles = new List<int>();

            foreach (Elevator item in elevators) {        

                if (item.currentFloor == 1 && item.status == "down"){
                    downs.Add(item.destination);
                } else if (item.currentFloor == 1 && item.status == "idle"){
                    idles.Add(item.id);
                }
            }

            if (downs.Count() != 0 ) {

                int down = getClosest(n, downs);
                
                foreach (Elevator item in elevators) {

                    if(item.currentFloor == 1 && item.status == "down" && item.destination == down){

                        Console.WriteLine("Elevator " + item.id + " is selected. Press enter.");
                        Console.ReadLine();

                        item.selected = true;
                        item.destination = n;
                        return;
                    } 
                }

            } else if (idles.Count() != 0) {

                Console.WriteLine("Elevator " + idles[0] + " is selected. Press enter.");
                Console.ReadLine();

                elevators[idles[0] - 1].selected = true;
                elevators[idles[0] -1].destination = n;
                return;

            } else {

                List<int> ups = new List<int>();

                foreach (Elevator item in elevators){
                    if (item.status == "up") {
                        ups.Add(item.currentFloor);
                    }
                }
            
                if (ups.Count() != 0) {
                    int up = getClosest(1, ups);
                
                    foreach (Elevator item in elevators) {

                        if (item.currentFloor == up && item.status == "up") {
                            Console.WriteLine("Elevator " + item.id + " is selected. Press enter.");
                            Console.ReadLine();

                            elevators[idles[0] - 1].selected = true;
                            elevators[idles[0] -1].destination = n;
                            return;
                        }
                    }
                } 

  
                List<int> others = new List<int>();

                foreach(Elevator item in elevators) {
                    others.Add(item.currentFloor);
                }

                int other = getClosest(n, others);
                
                foreach (Elevator item in elevators) {

                    if (item.currentFloor == other) {

                        Console.WriteLine("Elevator " + item.id + " is selected. Press enter.");
                        Console.ReadLine();

                        item.selected = true; 
                        item.destination = n;
                        return;
                    }
                }
            }
        }
    }
}

    class Elevator {
        public int id;
        public string status;
        public int currentFloor;
        public int destination; 
        public List<int> queue = new List<int>{};
        public bool selected;
        public string doors;
        public int capacity;
    

        public void move() {
        
            if (status != "idle") {

                if (status == "up" ) {

                    if (currentFloor == -1){
                        currentFloor = 1;     //Skip floor 0, which is not valid

                    } else {
                        currentFloor += 1;

                    }
                    Console.WriteLine("Elevator " + this.id + " is " + status + " and is at floor " + currentFloor + "\n");

                } else if (status == "down") {

                    if(currentFloor == 1){
                        currentFloor = -1;

                    } else {
                        currentFloor += -1;

                    }
                    Console.WriteLine("Elevator " + this.id + " is " + status + " and is at floor " + currentFloor + "\n");
                }
            }
        }

        public void selectDirection(int n) { //Make elevator move if it's starting from idle

            if (status == "idle") {

                if(currentFloor >= n){
                    status = "down";

                } else {
                    status = "up";
                }
            }
        }

        public void checkFloor() { 

                if (currentFloor == 1 && selected == true) { //Check if at RC for calls made on floors

                    Console.WriteLine("Elevator " + id + " is at RC. Press enter.");
                    Console.ReadLine();

                    doors = "open";
                    Console.WriteLine("Doors open");

                    Console.WriteLine("There is " + capacity + " persons inside");
                    Console.WriteLine("People are getting in and out. How many persons are now in the elevator?");
                    int z1 = Convert.ToInt32(Console.ReadLine());

                    while (z1 > 15 || z1 < 0){

                        Console.WriteLine("Elevator is empty or have 15 persons maximum!");
                        Console.WriteLine("How many persons are getting out?");
                        z1 = Convert.ToInt32(Console.ReadLine());
                    }

                    capacity = z1;

                    Console.WriteLine("Waiting for people to get out ...");
                    Console.WriteLine("There is now " + capacity + " person inside");
                    Console.WriteLine("Doors are now closing. Press enter.");
                    Console.ReadLine();

                    doors = "close";
                    selected = false;

                    if (destination != 0) {
                    queue.Add(destination);
                    selectDirection(destination); 
                    
                    }

                } else {
                    
                    for( int x = 0; x < queue.Count(); x++) {  //Check on floors not RC

                        if (currentFloor == queue[x]) {

                            Console.WriteLine("Elevator " + id + " arrived at floor " + currentFloor + ". Press enter.");
                            Console.ReadLine();

                            doors = "open";
                            Console.WriteLine("Doors open");

                            Console.WriteLine("There is " + capacity + " persons inside");
                            Console.WriteLine("People are getting in and out. How many persons is now in the elevator?");
                            int z = Convert.ToInt32(Console.ReadLine());

                            while ( z > 15 || z < 0){
                                Console.WriteLine("Elevator is empty or have 15 persons maximum!");
                                Console.WriteLine("How many persons are lucky enough to get in?");
                                z = Convert.ToInt32(Console.ReadLine());
                            }

                            capacity = z;

                            Console.WriteLine("There is now " + capacity + " person inside");
                            Console.WriteLine("Doors are closing. Press enter.");
                            Console.ReadLine();

                            doors = "close";
                            queue.RemoveAt(x);
                        }
                    }
                }

            if (queue.Count() != 0 && selected == false){ //Make elevator at RC go somewhere
                
                if (queue.Max() > 0 ){
                    status = "up";
                } else {
                    status = "down";
                }

            }
            
            if (queue.Count() == 0 && selected == true) {  //Go to RC if in the wrong direction

                    if (currentFloor > 0 && status == "up" ) { //For upper elevators
                        status = "down";

                    } else if (currentFloor < 0 && status == "down") {  //For lower elevators
                        status = "up"; 
                    }
            }

            if (queue.Count() == 0 && selected == false) { //Make elevator idle if no more calls 

                if (status != "idle"){
                    status = "idle";

                    if(capacity != 0){

                        Console.WriteLine("Elevator " + id + " has no more calls, but people are still inside!");
                        Console.WriteLine("THEY ARE TRAPPED FOREVER. Press enter to leave them to their fate.");
                        Console.ReadLine();
                    } 
                }
            }     
        }
    }
   



