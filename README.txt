All three controllers has interface working on the console.

Both the c# and go code include various additional requirements,
including making the elevators move and a capacity management for 
each elevators, just like I did last week. The interface will let you choose
the initial scenario that you want to try. 
Those codes are dynamic for the # of floors, basements, columns and elevator per column, you just have to
change these numbers when instantiating a controller. They are set to those required
for the scenario you gave us, but feel free to change them. The number of elevators deserved by each column
 is found by dividing topFloor/columns. If the modulo is not zero, the remaining floors are deserved by the top column.
One column deserve the basements. 

The JAVA code is simpler, but work as intended. You type in which scenario you want and it spits ou the selected elevator.
I didn't get the time to do like the other two, but it does what is asked!
THe code is located in src folder, in the java folder.

All comments are made in the c# file.

Thank you!
