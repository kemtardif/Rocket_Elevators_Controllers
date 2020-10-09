package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func main() {

	scann := bufio.NewScanner(os.Stdin)
	controller := newController(60, 6, 4, 5)

	fmt.Println("Choose which floor you're at: (Negative for basements and zero not a floor!)")
	scann.Scan()
	initial1 := scann.Text()
	initial, _ := strconv.Atoi(initial1)

	if initial == 1 {
		controller.assignElevator()
	} else {
		controller.requestElevator(initial)
	}

	for i := 0; i < 1; {
		for _, item := range controller.elevators {
			item.checkFloor()
			item.move()

		}
	}

}

type Controller struct {
	selectedColumn int
	deserving      int
	basements      int
	totalColumns   int
	upperFloor     int

	elevators []*Elevator
}

func newController(upper, bases, columns, elevPerColumns int) *Controller {

	c := new(Controller)

	for i := 0; i < elevPerColumns; i++ {

		c.elevators = append(c.elevators, &Elevator{})

	}

	c.basements = bases
	c.totalColumns = columns
	c.upperFloor = upper
	c.deserving = (upper - (upper % (columns - 1))) / (columns - 1)

	return c
}

func (s *Controller) requestElevator(n int) {
	s.selection(n)
	s.initialize()

	if n < 0 {
		s.requestBelow(n)
	} else {
		s.requestAbove(n)
	}
}

func (s *Controller) selection(n int) {

	if n >= -(s.basements-1) && n < 1 {

		s.selectedColumn = 0
		selected := string(s.selectedColumn + 65)

		fmt.Printf("Column %v is selected \n", selected)
		fmt.Printf("This column deserves %v basements \n", s.basements)

	} else if n > s.deserving*(s.totalColumns-2) && n <= s.upperFloor {

		s.selectedColumn = s.totalColumns - 1
		selected := string(s.selectedColumn + 65)

		x := s.deserving*(s.totalColumns-2) + 1
		fmt.Printf("Column %v is selected \n", selected)
		fmt.Printf("This column deserves floor %v up to %v \n", x, s.upperFloor)

	} else {
		for i := 0; i < s.totalColumns-2; i++ {

			if n > s.deserving*i && n <= s.deserving*(i+1) {
				s.selectedColumn = i + 1
				selected := string(s.selectedColumn + 65)

				y := s.deserving*i + 1
				z := s.deserving * (i + 1)
				fmt.Printf("Column %v is selected \n", selected)
				fmt.Printf("This column deserves floor %v up to %v \n", y, z)
			}
		}
	}

}

func (s *Controller) initialize() {
	scanner := bufio.NewScanner(os.Stdin)

	for i := 0; i < len(s.elevators); i++ {

		var a int = i + 1
		fmt.Printf("Elevator %d status is : ", a)
		scanner.Scan()
		st := scanner.Text()

		fmt.Printf("Elevator %d current floor is : ", a)
		scanner.Scan()
		f1 := scanner.Text()
		f, _ := strconv.Atoi(f1)

		if st != "idle" {

			fmt.Printf("Elevator %d destination is : ", a)
			scanner.Scan()
			d1 := scanner.Text()
			d, _ := strconv.Atoi(d1)

			if d == 1 {
				s.elevators[i].selected = true

			} else if d < f && st == "down" && d > 0 {
				s.elevators[i].selected = true
				s.elevators[i].queue = append(s.elevators[i].queue, d)

			} else if d > f && st == "up" && d < 0 {
				s.elevators[i].selected = true
				s.elevators[i].queue = append(s.elevators[i].queue, d)

			} else {
				s.elevators[i].selected = false
				s.elevators[i].queue = append(s.elevators[i].queue, d)

			}

			fmt.Println("How many persons are in this elevator?")
			scanner.Scan()
			z1 := scanner.Text()
			z, _ := strconv.Atoi(z1)

			for z > 15 || z < 0 {

				fmt.Println("Elevator is empty or have a maximum of 15!")
				fmt.Println("How many persons are in this elevator?")
				scanner.Scan()
				z1 = scanner.Text()
				z, _ = strconv.Atoi(z1)

			}

			s.elevators[i].capacity = z

		} else {
			s.elevators[i].capacity = 0

		}

		s.elevators[i].id = a
		s.elevators[i].status = st
		s.elevators[i].currentFloor = f
		s.elevators[i].destination = 0

	}
}

func (s *Controller) requestAbove(n int) {

	var ups []int
	var idles []int

	scanner := bufio.NewScanner(os.Stdin)

	for _, item := range s.elevators {
		if item.currentFloor >= n && item.status == "down" {
			ups = append(ups, item.currentFloor)
		} else if item.status == "idle" {
			idles = append(idles, item.currentFloor)
		}
	}

	if len(ups) != 0 {

		var up int = getClosest(n, ups)

		for _, item := range s.elevators {
			if item.currentFloor >= n && item.status == "down" && item.currentFloor == up {
				fmt.Printf("Elevator %d is selected. Press enter.", item.id)
				scanner.Scan()

				item.selected = true
				item.queue = append(item.queue, n)
				item.selectDirection(n)
				return
			}
		}
	} else if len(idles) != 0 {

		var idle int = getClosest(n, idles)

		for _, item := range s.elevators {
			if item.status == "idle" && item.currentFloor == idle {
				fmt.Printf("Elevator %d is selected. Press enter.", item.id)
				scanner.Scan()

				item.selected = true
				item.queue = append(item.queue, n)
				item.selectDirection(n)
				return
			}
		}
	}
	return
}

func (s *Controller) requestBelow(n int) {

	var downs []int
	var idles []int

	scanner := bufio.NewScanner(os.Stdin)

	for _, item := range s.elevators {

		if item.currentFloor <= n && item.status == "up" {
			downs = append(downs, item.currentFloor)
		} else if item.status == "idle" {
			idles = append(idles, item.currentFloor)
		}
	}

	if len(downs) != 0 {

		var down int = getClosest(n, downs)

		for _, item := range s.elevators {
			if item.currentFloor <= n && item.status == "up" && item.currentFloor == down {
				fmt.Printf("Elevator %d is selected. Press enter.", item.id)
				scanner.Scan()

				item.selected = true
				item.queue = append(item.queue, n)
				item.selectDirection(n)
				return
			}
		}
	} else if len(idles) != 0 {

		var idle int = getClosest(n, idles)

		for _, item := range s.elevators {
			if item.status == "idle" && item.currentFloor == idle {
				fmt.Printf("Elevator %d is selected. Press enter.", item.id)
				scanner.Scan()

				item.selected = true
				item.queue = append(item.queue, n)
				item.selectDirection(n)
				return
			}
		}
	}
	return
}

func getClosest(n int, ls []int) int {

	var minDistance []int

	for i := 0; i < len(ls); i++ {
		x := n - ls[i]
		if x < 0 {
			x = -x
		}
		minDistance = append(minDistance, x)
	}

	var min int = minDistance[0]
	for _, item := range minDistance {
		if item < min {
			min = item
		}
	}
	for i := 0; i < len(ls); i++ {
		if minDistance[i] == min {
			return ls[i]
		}
	}
	return min
}

func (s *Controller) assignElevator() {

	scanner := bufio.NewScanner(os.Stdin)

	fmt.Println("Select which floor you want to go to (Negative integers for basements, RC is 1 and 0 is not a floor.")
	scanner.Scan()
	n1 := scanner.Text()
	n, _ := strconv.Atoi(n1)

	s.selection(n)
	s.initialize()

	if n < 0 {
		s.lowerRC(n)
	} else {
		s.upperRC(n)
	}

}

func (s *Controller) upperRC(n int) {

	var ups []int
	var idles []int

	scanner := bufio.NewScanner(os.Stdin)

	for _, item := range s.elevators {

		if item.currentFloor == 1 && item.status == "up" {
			ups = append(ups, item.destination)
		} else if item.currentFloor == 1 && item.status == "idle" {
			idles = append(idles, item.id)
		}
	}

	if len(ups) != 0 {

		var up int = getClosest(n, ups)

		for _, item := range s.elevators {

			if item.currentFloor == 1 && item.status == "up" && item.destination == up {
				fmt.Printf("Elevator %d is selected. Press enter.", item.id)
				scanner.Scan()

				item.selected = true
				item.destination = n
				return
			}
		}
	} else if len(idles) != 0 {

		fmt.Printf("Elevator %d is selected. Press enter.", idles[0])
		scanner.Scan()

		s.elevators[idles[0]-1].selected = true
		s.elevators[idles[0]-1].destination = n
		return
	} else {

		var downs []int

		for _, item := range s.elevators {

			if item.status == "down" {
				downs = append(downs, item.currentFloor)
			}
		}

		if len(downs) != 0 {

			var down int = getClosest(1, downs)

			for _, item := range s.elevators {

				if item.currentFloor == down && item.status == "down" {
					fmt.Printf("Elevator %d is selected. Press enter.", item.id)
					scanner.Scan()

					item.selected = true
					item.destination = n
					return
				}
			}
		} else {

			var others []int

			for _, item := range s.elevators {
				others = append(others, item.currentFloor)
			}

			var other int = getClosest(n, others)

			for _, item := range s.elevators {
				if item.currentFloor == other {

					fmt.Printf("Elevator %d is selected. Press enter.", item.id)
					scanner.Scan()

					item.selected = true
					item.destination = n
					return
				}
			}
		}
	}
}

func (s *Controller) lowerRC(n int) {

	var downs []int
	var idles []int

	scanner := bufio.NewScanner(os.Stdin)

	for _, item := range s.elevators {

		if item.currentFloor == 1 && item.status == "down" {
			downs = append(downs, item.destination)
		} else if item.currentFloor == 1 && item.status == "idle" {
			idles = append(idles, item.id)
		}
	}

	if len(downs) != 0 {

		var down int = getClosest(n, downs)

		for _, item := range s.elevators {

			if item.currentFloor == 1 && item.status == "down" && item.destination == down {
				fmt.Printf("Elevator %d is selected. Press enter.", item.id)
				scanner.Scan()

				item.selected = true
				item.destination = n
				return
			}
		}

	} else if len(idles) != 0 {
		fmt.Printf("Elevator %d is selected. Press enter.", idles[0])
		scanner := bufio.NewScanner(os.Stdin)
		scanner.Scan()

		s.elevators[idles[0]-1].selected = true
		s.elevators[idles[0]-1].destination = n
		return

	} else {

		var ups []int

		for _, item := range s.elevators {
			if item.status == "up" {
				ups = append(ups, item.currentFloor)
			}
		}

		if len(ups) != 0 {
			var up int = getClosest(1, ups)

			for _, item := range s.elevators {
				if item.currentFloor == up && item.status == "up" {
					fmt.Printf("Elevator %d is selected. Press enter.", item.id)
					scanner.Scan()

					item.selected = true
					item.destination = n
					return
				}
			}
		}

		var others []int

		for _, item := range s.elevators {
			others = append(others, item.currentFloor)
		}

		var other int = getClosest(n, others)

		for _, item := range s.elevators {

			if item.currentFloor == other {
				fmt.Printf("Elevator %d is selected. Press enter.", item.id)
				scanner := bufio.NewScanner(os.Stdin)
				scanner.Scan()

				item.selected = true
				item.destination = n
				return

			}
		}
	}
}

type Elevator struct {
	id           int
	status       string
	currentFloor int
	destination  int
	queue        []int
	selected     bool
	doors        string
	capacity     int
}

func (s *Elevator) move() {

	if s.status != "idle" {

		if s.status == "up" {

			if s.currentFloor == -1 {
				s.currentFloor = 1

			} else {
				s.currentFloor++

			}
			fmt.Printf("Elevator %v is %v and is at floor %v \n", s.id, s.status, s.currentFloor)

		} else if s.status == "down" {

			if s.currentFloor == 1 {
				s.currentFloor = -1

			} else {
				s.currentFloor--

			}
			fmt.Printf("Elevator %v is %v and is at floor %v \n", s.id, s.status, s.currentFloor)
		}
	}
}

func (s *Elevator) selectDirection(n int) {

	if s.status == "idle" {

		if s.currentFloor >= n {
			s.status = "down"

		} else {
			s.status = "up"
		}
	}
}

func (s *Elevator) checkFloor() {

	scanner := bufio.NewScanner(os.Stdin)

	if s.currentFloor == 1 && s.selected == true {

		fmt.Printf("Elevator %v is at RC. Press enter.", s.id)
		scanner.Scan()

		s.doors = "open"
		fmt.Println("Doors open")

		fmt.Printf("There is %v persons inside. \n", s.capacity)
		fmt.Println("People are getting in and out. How many persons are inside now?")
		scanner.Scan()
		z := scanner.Text()
		z1, _ := strconv.Atoi(z)

		for z1 > 15 || z1 < 0 {
			fmt.Println("Elevator is empty or have 15 persons maximum!")
			fmt.Println("How many persons are inside?")
			scanner.Scan()
			z = scanner.Text()
			z1, _ = strconv.Atoi(z)
		}

		s.capacity = z1

		fmt.Println("Waiting for people to get out...")
		fmt.Printf(" There is now %v persons inside\n", s.capacity)
		fmt.Println("Doors are now closing. Press enter.")
		scanner.Scan()

		s.doors = "close"
		s.selected = false

		if s.destination != 0 {
			s.queue = append(s.queue, s.destination)
			s.selectDirection(s.destination)

		}

	} else {
		for x := 0; x < len(s.queue); x++ {

			if s.currentFloor == s.queue[x] {

				fmt.Printf("Elevator %v is arrived at floor %v. Press enter", s.id, s.currentFloor)
				scanner.Scan()

				s.doors = "open"
				fmt.Println("Doors open")

				fmt.Printf("There is %v persons inside.\n", s.capacity)
				fmt.Println("People are getting in and out. How many persons are inside now?")
				scanner.Scan()
				z := scanner.Text()
				z1, _ := strconv.Atoi(z)

				for z1 > 15 || z1 < 0 {
					fmt.Println("Elevator is empty or have 15 persons maximum!")
					fmt.Println("How many are lucky enough te be in?")
					scanner.Scan()
					z = scanner.Text()
					z1, _ = strconv.Atoi(z)
				}

				s.capacity = z1

				fmt.Println("Waiting for people to get out...")
				fmt.Printf(" There is now %v persons inside \n", s.capacity)
				fmt.Println("Doors are now closing. Press enter.")
				scanner.Scan()

				s.doors = "close"
				for i, j := range s.queue {
					if j == s.currentFloor {

						s.queue = append(s.queue[:i], s.queue[i+1:]...)
					}
				}

			}
		}
	}

	if len(s.queue) != 0 && s.selected == false {
		var max int = s.queue[0]

		for _, value := range s.queue {
			if max < value {
				max = value
			}
		}

		if max > 0 {
			s.status = "up"
		} else {
			s.status = "down"
		}

	}

	if len(s.queue) == 0 && s.selected == true {

		if s.currentFloor > 0 && s.status == "up" {
			s.status = "down"

		} else if s.currentFloor < 0 && s.status == "down" {
			s.status = "up"
		}
	}

	if len(s.queue) == 0 && s.selected == false {

		if s.status != "idle" {
			s.status = "idle"

			if s.capacity != 0 {

				fmt.Printf("Elevator %v has no more calls, but people are still inside!\n", s.id)
				fmt.Println("THEY ARE TRAPPED FOREVER. Press enter to leave them to their fate.")
				scanner.Scan()
			}
		}
	}
}
