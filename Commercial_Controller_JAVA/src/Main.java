public class Main {

    public static void main(String[] args) {
        Controller controller = new Controller();

        System.out.println("Choose which floor you're at");
        int n = controller.scanner.nextInt();

        if (n == 1) {
            controller.assignElevator();
        } else {
            controller.requestElevator(n);
        }

        controller.scanner.nextLine();
    }
}
