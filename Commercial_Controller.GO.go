package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func main() {

	scanner := bufio.NewScanner(os.Stdin)

	controller := &Controller{}
	fmt.Println("Choose which floor you're at: ")
	scanner.Scan()
	initial1 := scanner.Text()
	initial, _ := strconv.Atoi(initial1)

	if initial == 1 {

		controller.assignElevator()
	} else {

		controller.requestElevator(initial)
	}

}

type Elevator struct {
	id           int
	status       string
	currentFloor int
	destination  int
}

type Controller struct {
	columns   [4]int
	elevators []Elevator
}

func (s *Controller) requestElevator(n int) {
	s.initialize()

	if n < 0 {
		s.requestBelow(n)
	} else {
		s.requestAbove(n)
	}
}

func (s *Controller) selection(n int) {
	if n < 0 && n > -6 {
		fmt.Println("Basement column is selected")
		(*s).columns[0] = 1
		return

	} else if n > 0 && n < 21 {
		fmt.Println("Column A is selected")
		(*s).columns[1] = 1
		return

	} else if n > 20 && n < 41 {
		fmt.Println("Column B is selected")
		(*s).columns[2] = 1
		return

	} else if n > 40 && n < 61 {
		fmt.Println("Column C is selected")
		(*s).columns[3] = 1
		return

	}
}

func (s *Controller) initialize() []Elevator {
	scanner := bufio.NewScanner(os.Stdin)
	for i := 0; i < 5; i++ {
		var a int = i + 1
		fmt.Printf("Elevator %d status is : ", a)
		scanner.Scan()
		st := scanner.Text()

		fmt.Printf("Elevator %d current floor is : ", a)
		scanner.Scan()
		f1 := scanner.Text()
		f, _ := strconv.Atoi(f1)

		d := 0
		if st != "idle" {
			fmt.Printf("Elevator %d destination is : ", a)
			scanner.Scan()
			d1 := scanner.Text()
			d, _ = strconv.Atoi(d1)
		}
		var x Elevator = Elevator{id: a, status: st, currentFloor: f, destination: d}
		s.elevators = append(s.elevators, x)

	}
	return s.elevators

}

func (s *Controller) requestAbove(n int) {
	var ups []int
	var idles []int

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
				fmt.Printf("Elevator %d is selected.", item.id)
				return
			}
		}
	} else if len(idles) != 0 {

		var idle int = getClosest(n, idles)

		for _, item := range s.elevators {
			if item.status == "idle" && item.currentFloor == idle {
				fmt.Printf("Elevator %d is selected.", item.id)
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
			fmt.Printf("Elevator %d is selected.", item.id)
			return
		}
	}

	return
}

func (s *Controller) requestBelow(n int) {
	var downs []int
	var idles []int

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
				fmt.Printf("Elevator %d is selected.", item.id)
				return
			}
		}
	} else if len(idles) != 0 {

		var idle int = getClosest(n, idles)

		for _, item := range s.elevators {
			if item.status == "idle" && item.currentFloor == idle {
				fmt.Printf("Elevator %d is selected.", item.id)
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
			fmt.Printf("Elevator %d is selected.", item.id)
			return
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
	return 0
}

func (s *Controller) callAnswered(n int) {

	if n < 0 && n > -6 {
		s.columns[0] = 0
		return

	} else if n > 0 && n < 21 {
		s.columns[1] = 0
		return

	} else if n > 20 && n < 41 {
		s.columns[2] = 0
		return

	} else if n > 40 && n < 61 {
		s.columns[3] = 0
		return

	}
}

func (s *Controller) assignElevator() {

	scanner := bufio.NewScanner(os.Stdin)
	fmt.Println("Select which floor you want to go to")
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

	s.callAnswered(n)

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
				fmt.Printf("Elevator %d selected.", item.id)
				return
			}
		}
	} else if len(idles) != 0 {
		fmt.Printf("Elevator %d is selected.", idles[0])
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
					fmt.Printf("Elevator %d is selected.", item.id)
					return
				}
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
			fmt.Printf("Elevator %d is selected.", item.id)
			return
		}
	}
	return
}

func (s *Controller) lowerRC(n int) {

	var downs []int
	var idles []int

	s.callAnswered(n)

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
				fmt.Printf("Elevator %d is selected.", item.id)
				return
			}
		}

	} else if len(idles) != 0 {
		fmt.Printf("Elevator %d is selected.", idles[0])
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
					fmt.Printf("Elevator %d is selected.", item.id)
					return
				}
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
			fmt.Printf("Elevator %d is selected.", item.id)
			return
		}
	}

	return
}
