
#CONTROLLER OBJECT

package Controller;

use strict;
use warnings;
use List::Util qw(min max);

sub new{
    my $class = shift;
    my $self = {
        column => (),
        calls => (),

    };

    bless $self, $class;
    return $self;
}
 
sub findDirection {
    my ($self, $a, $c) = @_;

    my @c = @{$_[2]};

        if ($a->{floor} > $c[0]) {
            $a->{direction} = "down";
        } elsif ($a->{floor} < $c[0]){
            $a ->{direction} = "up";
        }
}
    
sub getClosest {
    my ($self, $a, $b, $c) = @_;
    my @c = @$c;
    my $absA = abs($a->{floor} - $c[0]);
    my $absB = abs($b->{floor} - $c[0]);
    if ($absA > $absB) {
        push(@{$b->{queue}}, $c[0]);
        $self->{calls} = grep {$_ ne @c} $self->{calls};
        print "Elevator B is selected";
        if ($b->{floor} - $c[0] > 0){
            $b->{direction} = "down";
        } elsif ($b->{floor}-$c[0] < 0) {
            $b->{direction} = "up";
        }
    } elsif ($absB > $absA) {
        push(@{$a->{queue}}, $c[0]);
        $self->{calls} = grep {$_ ne @c} $self->{calls};
        print "Elevator A is selected";
        if ($a->{floor} - $c[0] > 0){
            $a->{direction} = "down";
        } elsif ($a->{floor} - $c[0] < 0) {
            $a->{direction} = "up";
        }
    } else {
        push(@{$a->{queue}}, $c[0]);
        $self->{calls} = grep {$_ ne @c} $self->{calls};
        $self->findDirection($a, @c);
        print "Elevator A is selected";
    }
}

sub requestElevator {
    my ($self, $a, $b, $c) = @_;
    my @c = @$c;
        
    if ($a->{direction} == "idle" && $b->{direction} == "idle") {  #Both are idle
        $self-> getClosest($a, $b, \@c);
    } elsif ($a->{direction} != "idle" && $b->{direction} == "idle") { #A is moving, B is idle
        if ($c[1] == "up") {
            if ($a->{direction} == "up" && $c[0] > $a->{floor}){
                push(@{$a->{queue}}, $c[0]);
                print "Elevator A is selected";
                $self->{calls} = grep {$_ ne @c} $self->{calls};
            } else {
                push(@{$b->{queue}}, $c[0]);
                print "Elevator B is selected";
                $self->{calls} = grep {$_ ne @c} $self->{calls};
                $self->findDirection($b, \@c);
            } else {
                 if ($a->{direction} == "down" && $c[0] < $a->{floor}) {
                push $a->{queue}, $c[0];
                print "Elevator A is selected";
                $self->{calls} = grep {$_ ne @c} $self->{calls};
            }} else {
                push($b->{queue}, $c[0]);
                print "Elevator B is selected";
                $self->{calls} = grep {$_ ne @c} $self->{calls};
                $self->findDirection($b, \@c);
            }
             }
      } elsif ($b->{direction} != "idle" && $a->{direction} == "idle") { #B is moving, A is idle
            if ($c[1] == "up") {
                if ($b->{direction} == "up" && $c[0] > $b->{floor}) {
                    push($b->{queue}, $c[0]);
                    print "Elevator B is selected ";
                    $self->{calls} = grep {$_ ne @c} $self->{calls};
                } else {
                    push($a->{queue}, $c[0]);
                    print "Elevator A is selected";
                    $self->{calls} = grep {$_ ne @c} $self->{calls};
                    $self->findDirection($a, \@c)
                }
            } else {
                if ($b->{direction} == "down" && $c[0] < $b->{floor}) {
                    push($b->{queue}, $c[0]);
                    print "Elevator B is selected";
                    $self->{calls} = grep {$_ ne @c} $self->{calls};
                } else {
                    push($a->{queue}, $c[0]);
                    print "Elevator A is selected";
                    $self->{calls} = grep {$_ ne @c} $self->{calls};
                    $self->findDirection($a, \@c);
               }
            }
        } elsif ($a->{direction} == "up" && $b->{direction} == "up" && $c[1] == "up") { #Both are going up and up call
                if ($c[0] > $a->{floor} && $c[0] > $b->{floor}) {
                    self.getClosest(a, b, c);
                } elsif ($c[0] > $a->{floor}) {
                    push($a->{queue}, $c[0]);
                    print "Elevator A is selected";
                    $self->{calls} = grep {$_ ne @c} $self->{calls};
                } elsif ($c[0] > $b->{floor}) {
                    push($b->{queue}, $c[0]);
                    puts "Elevator B is selected";
                    $self->{calls} = grep {$_ ne @c} $self->{calls};
                }
        }elsif ($a->{direction} == "down" && $b->{direction} == "down" && $c[1] == "down") { #Both are going down and down call
            if ($c[0] < $a->{floor} && $c[0] < $b->{floor}) {
                self->getClosest($a, $b, \@c);
            } elsif ($c[0] < $a->{floor}) {
                push($a->{queue}, $c[0]);
                print"Elevator A is selected";
                $self->{calls} = grep {$_ ne @c} $self->{calls};
            } elsif ($c[0] < $b->{floor}) {
                push($b->{queue}, $c[0]);
                puts"Elevator B is selected";
                $self->{calls} = grep {$_ ne @c} $self->{calls};
            }
        } elsif ($a->{direction} != "idle" && $b->{direction} != "idle" && $a->{direction} != $b->{direction}) { #Opposite direction
            if ($c[1] == "up") {
                if ($a->{direction} == "up" && $c[0] > $a->{floor}) {
                    push($a->{queue}, $c[0]);
                    print "Elevator A is selected";
                    $self->{calls} = grep {$_ ne @c} $self->{calls};
                } elsif ($b->{direction} == "up" && $c[0] > $b->{floor}) {
                    push($b->{queue}, $c[0]);
                    puts "Elevator B is selected";
                    $self->{calls} = grep {$_ ne @c} $self->{calls};
                }}
            } else {
                if ($a->{direction} == "down" && $c[0] < $a->{floor}) {
                    push($a->{queue}, $c[0]);
                    print "Elevator A is selected";
                    $self->{calls} = grep {$_ ne @c} $self->{calls};
                } elsif ($b->{direction} == "down" && $c[0] < $b->{floor}) {
                    push($b->{queue}, $c[0]);
                    print "Elevator B is selected";
                    $self->{calls} = grep {$_ ne @c} $self->{calls};
                }
            }
    }



    sub selection {
        my ($self, $a, $b) = @_;

        print "Select the floor you're at:";
        $f = <STDIN>;
        $f = chomp($f);
        print "You are at floor" + $f;
        print "Select which direction you are going:";
        $d = <STDIN>;
        $d = chomp($d);
        print "You want to go " + $d
        @c = [$f, $d];
        my $call = \@c;
        push($self->{calls}, @c);
        $self->requestElevator($a, $b, $call);
    }

    sub setup {
        my ($self, $a, $b) = @_;
        @c = [$a, $b];
        print "We first need to setup the inital configurations";
        for my $i (@c) {
            print "First choose Elevator " + $i->{id} + " initial floor: ";
            $i->{floor} = <STDIN>;
            $i->{floor} = chomp($i->{floor});
            print "Now select Elevator " + i.id + " initial direction:";
            $i->{direction} = <STDIN>;
            $i->{direction} = chomp($i->{direction})
                if ($i->{direction} != "idle") {
                    print "Select Elevator " + i.id + " destination: ";
                    $k = <STDIN>;
                    $k = chomp($k);
                    push($i->{selected, $k};)
                    print "How many persons are in the elevator? ";
                    $i->{capacity} = <STDIN>;
                    while ($i->{capacity} > 15 || i.capacity < 0) {
                        print "Elevator is empty or with 15 persons maximum!";
                        print "How many persons are in the elevator? ";
                        $i->{capacity} = <STDIN>;
                    }
                }
            }
            $self->selection($a, $b);
    }

    sub moveColumn {
        my ($self, $a, $b) = @_;
        while (scalar($a->{queue}) != 0 || scalar($a->{selected}) != 0 || scalar($b->{queue}) != 0 || scalar($b->{selected}) != 0) {
            for my $x ($self->{column}) {
                if (scalar($x->{queue}) == 0 && scalar($x->{selected}) == 0) {
                        $x->{direction} = "idle";
                }
            }
            for $x ($self->{column}) {
                $x->move();
                $x->checkFloor();
            }
            for $x ($self->{calls}){
                $self->requestElevator($a, $b, $x)
            }
            sleep(1)
        }
    }

1;