# USUALLY YOU'D HAVE DIFFERENT PACKAGES FOR DIFFERENT CLASSES
#BUT FOR THE SAKE OF SIMPLICITY I JUST PUT BOTH CLASSES IN THE SAME FILE

#ELEVATOR OBJECT

package Elevator;

use strict;
use warnings;
use List::Util qw(min max);

sub new {
    my $class = shift;
    my $self = {   
        id => shift,
        floor => shift,
        direction => shift,
        door => shift,
        queue => [],
        selected => [],
        capacity => 0,
        restFloor => shift,
    };
    bless $self, $class;
    return $self;
}
        
sub open {
    my ($self) = @_;
    $self->{door} = "open";

}

sub close {
    my ($self) = @_;
    $self->{door} = "closed";
}
        
sub move {
    my ($self) = @_;

    if ($self->{direction} != "idle"){
        if ($self->{direction} == "up" && $self->{floor} < 10){
            $self->{floor} += 1;
        } elsif ($self->{direction} == "down" && $self->{floor} > 1) {
            $self->{floor} -= 1;
        }
        print "Elevator " + $self->{id} + " is moving " + $self->{direction} + " and is at floor " + $self->{floor};
    }
}
sub requestFloor {
    my ($self) = @_;
    print "Select destination:";
    my $n = <STDIN>;
    chomp($n);
    print "You selected floor " + $n;
    if (scalar($self->{queue}) == 0 && $self->{direction} == "idle") {
        if ($self->{floor} > $n) {
            $self->{direction} = "down";
        } elsif ($self->{direction} < $n){
            $self->{direction} = "up";
        }
    }
    push(@{$self->{selected}}, $n);
}

sub checkFloor {
    my ($self) = @_;
    foreach my $x ($self->{queue}) {

        if ($self->{floor} == $x) {
            print "Elevator " + $self->{id} + " arrived at floor " + $self->{floor};
            $self->open();
            print "Doors open";
            print "There is " + $self->{capacity} + " person inside";
           print "How many persons are getting in?";
            my $z = <STDIN>;
            $z = chomp($z);
            while ($self->{capacity} + $z > 15 || $z < 0) {
                print "Elevator is empty or have at most 15 persons!";
                print " How many persons are lucky enough to get in?";
                $z = <STDIN>;
            }
            $self->{capacity} += $z;
            print "Waiting for people to get in...";
            sleep(3);
            print "There is now " + $self->{capacity} + " persons inside";
            print "Doors are now closing";

            $self->close();
            $self->{queue} = grep {$_ ne $x} $self->{queue};
            $self->requestFloor();
        }
    }
        
    foreach my $x ($self->{selected}){
        if ($self->{floor} == $x) {
            print "Elevator " + $self->{id} + " arrived at it's destination";
            $self->open();
            print "There is " + $self->{capacity} + " person inside";
            print "How many persons are getting out?";
            my $z1 = <STDIN>;
            $z1 = chomp($z1);

            while ($z1 > $self->{capacity} || $z1 < 0) {
                print "Elevator is empty or have at most 15 persons!";
                print " How many persons are getting out?";
                $z1 = <STDIN>;
                $z1 = chomp($z1);
            }

            $self->{capacity} -= $z1;

            print "Waiting for people to get out...";
            sleep(3);
            print "There is now " + $self->{capacity} + " persons inside";
            print "Doors are now closing";
                
            $self->close();
            $self->{selected} = grep{$_ ne $x} $self->{capacity};
        }
    }

    if (scalar($self->{selected}) != 0 && scalar($self->{queue}) == 0){
        if ($self->{direction} == "up" && $self->{floor} > max($self->{selected})) {
            $self->{direction} = "down";
        } elsif ($self->{direction} == "down" && $self->{floor} < min($self->{selected})){
            $self->{direction} = "up";
        }
    }
        

    if (scalar($self->{queue}) == 0 && scalar($self->{selected}) == 0) {
        $self->{direction} = "idle";
        if ($self->{capacity} != 0) {
            print "Elevator " + $self->{id} + " has no more calls, but there's still people inside!";
            print "Where do they wanna go?";
            $self->requestFloor();
        }
    }


}

1;