using System;
using System.Linq;
using System.Collections.Generic;

namespace Commercial_Controller
{
    class Program
    {
        static void Main(string[] args)
        {
            Controller controller = new Controller();

            Console.WriteLine("Choose which floor you're at");
            int n = Convert.ToInt32(Console.ReadLine());
            if (n == 1) {
                controller.assignElevator();
            } else {
                 controller.requestElevator(n);
            }

            Console.ReadLine();

        }
    }

    class Controller {
        public int[] columns = new int[4];
        public List<Elevator> elevators = new List<Elevator>(){
                new Elevator(),
                new Elevator(),
                new Elevator(),
                new Elevator(),
                new Elevator(),
        }; ///status current floor, destination

        public void requestElevator(int n) {
            initialize();
            if (n < 0) {
                requestBelow(n);
            } else {
                requestAbove(n);
            }
        }

        public void selection(int n) {

            if (n < 0 && n > -6) {
                Console.WriteLine("Basement column is selected");
                columns[0] = 1;
                return;

            } else if (n > 0 && n < 21) {
                Console.WriteLine("Column A is selected");
                columns[1] = 1;
                return;

            }else if (n > 20 && n < 41) {
                Console.WriteLine("Column B is selected");
                columns[2] = 1;
                return;

            } else if (n > 40 && n < 61) {
                Console.WriteLine("Column C is selected");
                columns[3] = 1;
                return;

            }
        }

        public void initialize () {

            for (int i = 0; i < 5; i++){

                int a = i + 1;
                Console.WriteLine("Elevator " + a + " status is:");
                string s1 = Console.ReadLine();
                Console.WriteLine("Elevator " + a + " current floor is:");
                int f1 = Convert.ToInt32(Console.ReadLine());
                int d1 = 0;
                if ( s1 != "idle" ) {
                Console.WriteLine("Elevator " + a + " destination is: ");
                    d1 = Convert.ToInt32(Console.ReadLine());
                } 
                elevators[i].id = a;
                elevators[i].status = s1;
                elevators[i].currentFloor = f1;
                elevators[i].destination = d1;
            }
        }

        public void requestAbove(int n) {
            List<int> ups = new List<int>();
            List<int> idles = new List<int>();


            foreach (Elevator item in elevators) {         
                if (item.currentFloor >= n && item.status == "down"){
                    ups.Add(item.currentFloor);
                } else if (item.status == "idle"){
                    idles.Add(item.currentFloor);
                }
             }
        
             if (ups.Count() != 0) {

                int up = getClosest(n, ups);

                foreach (Elevator item in elevators) {
                    if(item.currentFloor >= n && item.status == "down" && item.currentFloor == up){
                        Console.WriteLine("Elevator " + item.id + " is selected.");
                        return;
                    } 
                }
             } else if (idles.Count() != 0){

                int idle = getClosest(n, idles);

                foreach (Elevator item in elevators) {
                    if ( item.status == "idle" && item.currentFloor == idle) {
                        Console.WriteLine("Elevator " + item.id + " is selected.");
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
                    Console.WriteLine("Elevator " + item.id + " is selected.");
                    return;
                }
            }


            return;
        }

        public void requestBelow(int n) {
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
                        Console.WriteLine("Elevator " + item.id + " is selected.");
                        return;
                    } 
                }
            } else if (idles.Count() != 0){

                int idle = getClosest(n, idles);

                foreach (Elevator item in elevators) {
                    if ( item.status == "idle" && item.currentFloor == idle) {
                        Console.WriteLine("Elevator " + item.id + " is selected.");
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
                    Console.WriteLine("Elevator " + item.id + " is selected.");
                    return;
                }
            }


            return;
        }

        public int getClosest(int n, List<int> ls) {   
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

        public void callAnswered(int n) {

            if (n < 0 && n > -6) {
                columns[0] = 0;
                return;

            } else if (n > 0 && n < 21) {
                columns[1] = 0;
                return;

            }else if (n > 20 && n < 41) {
                columns[2] = 0;
                return;

            } else if (n > 40 && n < 61) {
                columns[3] = 0;
                return;

            }
        }

        public void assignElevator() {

            Console.WriteLine("Select which floor you want to go to");
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

            callAnswered(n);

            foreach (Elevator item in elevators) {         
                if (item.currentFloor == 1 && item.status == "up"){
                    ups.Add(item.destination);
                } else if (item.currentFloor == 1 && item.status == "idle"){
                    idles.Add(item.id);
                }
             }

             if (ups.Count() != 0 ) {

             int up = getClosest(n, ups);
             
             foreach (Elevator item in elevators) {
                 if(item.currentFloor == 1 && item.status == "up" && item.destination == up){
                    Console.WriteLine("Elevator " + item.id + " is selected.");
                     return;
                 } 
             }
             } else if (idles.Count() != 0) {
                    Console.WriteLine("Elevator " + idles[0] + " is selected.");
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
                            Console.WriteLine("Elevator " + item.id + " is selected.");
                            return;
                        }
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
                    Console.WriteLine("Elevator " + item.id + " is selected.");
                    return;
                }
            }

            return;
        }

        public void lowerRC(int n) {

            List<int> downs = new List<int>();
            List<int> idles = new List<int>();

            callAnswered(n);

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
                        Console.WriteLine("Elevator " + item.id + " is selected.");
                        return;
                    } 
                }

            } else if (idles.Count() != 0) {
                Console.WriteLine("Elevator " + idles[0] + " is selected.");
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
                            Console.WriteLine("Elevator " + item.id + " is selected.");
                            return;
                        }
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
                    Console.WriteLine("Elevator " + item.id + " is selected.");
                    return;
                }
            }

            return;
        }
         
    }

    class Elevator {
        public int id;
        public string status;
        public int currentFloor;
        public int destination;


        }
   
}


