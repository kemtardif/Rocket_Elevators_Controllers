
#Setting up the scenarios

use lib 'lib';
use Elevator;
use Controller;
use strict;
use warnings;
use List::Util qw(min max);

my $controller = new Controller();
my $elevatorA = new Elevator("A", 2, "idle", "closed", 1)
my $elevatorB = new Elevator("B", 6, "idle", "closed", 5)
push($controller->{column, $elevatorA};
push($controller->{column}, $elevatorB);


$controller->setup($elevatorA, $elevatorB);

$variable = 1;
while ($variable == 1) {
    
    $controller->moveColumn($elevatorA, $elevatorB);

    print "Both elevators are now empty, waiting for another call";
    $controller->selection($elevatorA, $elevatorB);

}