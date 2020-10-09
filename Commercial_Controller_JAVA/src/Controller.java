import java.util.*;

public class Controller {
    private String selectedColumn;
    private List<Elevator> elevators = new ArrayList<>();

    public Scanner scanner = new Scanner(System.in);

    public Controller() {
        for (int i = 0; i < 5; i++){

            this.elevators.add( new Elevator());
        }
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

    public void selection(int n) {

        if (n < 0 && n > -6) {
            selectedColumn = "Basement";

        } else if (n > 0 && n < 21) {
            selectedColumn = "A";

        }else if (n > 20 && n < 41) {
            selectedColumn = "B";

        } else if (n > 40 && n < 61) {
            selectedColumn = "C";

        }
        System.out.println("Column " + selectedColumn + " is selected");
    }

    public void initialize () {

        for (int i = 0; i < 5; i++){

            int a = i + 1;
            System.out.println("Elevator " + a + " status is:");
            scanner.nextLine();
            String s1 = scanner.nextLine();
            System.out.println("Elevator " + a + " current floor is:");
            int f1 = scanner.nextInt();
            int d1 = 0;
            if ( !s1.equals("idle") ) {
                System.out.println("Elevator " + a + " destination is: ");
                d1 = scanner.nextInt();
            }
            this.elevators.get(i).id = a;
            this.elevators.get(i).status = s1;
            this.elevators.get(i).currentFloor = f1;
            this.elevators.get(i).destination = d1;
        }
    }

    public void requestAbove(int n) {
        List<Integer> ups = new ArrayList<>();
        List<Integer> idles = new ArrayList<>();


        for (Elevator item : this.elevators) {
            if (item.currentFloor >= n && item.status.equals("down")) {
                ups.add(item.currentFloor);
            } else if (item.status.equals("idle")) {
                idles.add(item.currentFloor);
            }
        }

        if (ups.size() != 0) {

            int up = getClosest(n, ups);

            for (Elevator item : elevators) {
                if(item.currentFloor >= n && item.status.equals("down") && item.currentFloor == up){
                    System.out.println("Elevator " + item.id + " is selected.");
                    return;
                }
            }
        } else if (idles.size() != 0){

            int idle = getClosest(n, idles);

            for (Elevator item : elevators) {
                if ( item.status.equals("idle") && item.currentFloor == idle) {
                    System.out.println("Elevator " + item.id + " is selected.");
                    return;
                }
            }

        }

        List<Integer> others = new ArrayList<>();
        for (Elevator item : elevators) {
            others.add(item.currentFloor);
        }

        int other = getClosest(n, others);

        for (Elevator item : elevators) {
            if (item.currentFloor == other) {
                System.out.println("Elevator " + item.id + " is selected.");
                return;
            }
        }


    }

    public void requestBelow(int n) {
        List<Integer> downs = new ArrayList<>();
        List<Integer> idles = new ArrayList<>();

        for (Elevator item : elevators) {
            if (item.currentFloor <= n && item.status.equals("up")) {
                downs.add(item.currentFloor);
            } else if (item.status.equals("idle")) {
                idles.add(item.currentFloor);
            }
        }

        if (downs.size() != 0){

            int down = getClosest(n, downs);

            for (Elevator item : elevators) {
                if(item.currentFloor <= n && item.status.equals("up") && item.currentFloor == down){
                    System.out.println("Elevator " + item.id + " is selected.");
                    return;
                }
            }
        } else if (idles.size() != 0){

            int idle = getClosest(n, idles);

            for (Elevator item : elevators) {
                if ( item.status.equals("idle") && item.currentFloor == idle) {
                    System.out.println("Elevator " + item.id + " is selected.");
                    return;
                }
            }
        }

        List<Integer> others = new ArrayList<>();

        for (Elevator item : elevators) {
            others.add(item.currentFloor);
        }

        int other = getClosest(n, others);

        for (Elevator item : elevators) {
            if (item.currentFloor == other) {
                System.out.println("Elevator " + item.id + " is selected.");
                return;
            }
        }

    }

    public int getClosest(int n, List<Integer> ls) {
        List<Integer> minDistance = new ArrayList<>();
        for (int i = 0; i < ls.size(); i++) {
            minDistance.add(Math.abs(n - ls.get(i)));
        }
        int min = Collections.min(ls);

        for (int i = 0; i < ls.size(); i++ ){
            if (minDistance.get(i) == min){
                return ls.get(i);
            }
        }
        return min;
    }

    public void assignElevator() {

        System.out.println("Select which floor you want to go to");
        int n = scanner.nextInt();

        selection(n);
        initialize();

        if (n < 0) {
            lowerRC(n);
        } else {
            upperRC(n);
        }


    }

    public void upperRC(int n) {

        List<Integer> ups = new ArrayList<>();
        List<Integer> idles = new ArrayList<>();

        for (Elevator item : elevators) {
            if (item.currentFloor == 1 && item.status.equals("up") ){
                ups.add(item.destination);
            } else if (item.currentFloor == 1 && item.status.equals("idle") ){
                idles.add(item.id);
            }
        }

        if (ups.size() != 0 ) {

            int up = getClosest(n, ups);

            for (Elevator item : elevators) {
                if(item.currentFloor == 1 && item.status.equals("up") && item.destination == up){
                    System.out.println("Elevator " + item.id + " is selected.");
                    return;
                }
            }
        } else if (idles.size() != 0) {
            System.out.println("Elevator " + idles.get(0) + " is selected.");
            return;
        } else {
            List<Integer> downs = new ArrayList<>();

            for (Elevator item : elevators){
                if (item.status.equals("down")) {
                    downs.add(item.currentFloor);
                }
            }
            if (downs.size() != 0) {
                int down = getClosest(1, downs);

                for (Elevator item : elevators) {
                    if (item.currentFloor == down && item.status.equals("down")) {
                        System.out.println("Elevator " + item.id + " is selected.");
                        return;
                    }
                }
            }
        }

        List<Integer> others = new ArrayList<>();
        for (Elevator item : elevators) {
            others.add(item.currentFloor);
        }

        int other = getClosest(n, others);

        for (Elevator item : elevators) {
            if (item.currentFloor == other) {
                System.out.println("Elevator " + item.id + " is selected.");
                return;
            }
        }

    }

    public void lowerRC(int n) {

        List<Integer> downs = new ArrayList<>();
        List<Integer> idles = new ArrayList<>();

        for (Elevator item : elevators) {
            if (item.currentFloor == 1 && item.status.equals("down")) {
                downs.add(item.destination);
            } else if (item.currentFloor == 1 && item.status.equals("idle")) {
                idles.add(item.id);
            }
        }

        if (downs.size() != 0 ) {

            int down = getClosest(n, downs);

            for (Elevator item : elevators) {
                if(item.currentFloor == 1 && item.status.equals("down") && item.destination == down){
                    System.out.println("Elevator " + item.id + " is selected.");
                    return;
                }
            }

        } else if (idles.size() != 0) {
            System.out.println("Elevator " + idles.get(0) + " is selected.");
            return;
        } else {

            List<Integer> ups = new ArrayList<>();

            for (Elevator item : elevators){
                if (item.status.equals("up")) {
                    ups.add(item.currentFloor);
                }
            }

            if (ups.size() != 0) {
                int up = getClosest(1, ups);

                for (Elevator item : elevators) {
                    if (item.currentFloor == up && item.status.equals("up")) {
                        System.out.println("Elevator " + item.id + " is selected.");
                        return;
                    }
                }
            }
        }

        List<Integer> others = new ArrayList<>();

        for (Elevator item : elevators) {
            others.add(item.currentFloor);
        }

        int other = getClosest(n, others);

        for (Elevator item : elevators) {
            if (item.currentFloor == other) {
                System.out.println("Elevator " + item.id + " is selected.");
                return;
            }
        }

    }
}
