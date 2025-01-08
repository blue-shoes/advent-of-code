package main

import (
	"fmt"
	"math"
)

func mainPart1(presentGoal int) {
	elfSum := presentGoal / 10

	minPossible := int(math.Ceil(-1+math.Sqrt(float64(1+4*elfSum))) / 2)

	testNumber := minPossible
	for {
		sum := testNumber + 1
		for i := 2; i*i <= testNumber; i++ {
			if testNumber%i == 0 {
				sum += i
				sum += testNumber / i
			}
		}
		if sum >= elfSum {
			break
		}
		testNumber++
	}
	fmt.Printf("Minimum house number is %d.\n", testNumber)
}

func mainPart2(presentGoal int) {
	elfSum := presentGoal/11 + 1
	minPossible := int(math.Ceil(-1+math.Sqrt(float64(1+4*elfSum))) / 2)

	testNumber := minPossible
	for {
		sum := testNumber
		for i := 2; i <= 50; i++ {
			if testNumber%i == 0 {
				factor := testNumber / i
				if factor <= 50 {
					sum += i
				}
				sum += factor
			}
		}
		if sum >= elfSum {
			break
		}
		testNumber++
	}
	fmt.Printf("Minimum house number is %d.\n", testNumber)
}

func main() {
	presentGoal := 33100000

	mainPart1(presentGoal)
	mainPart2(presentGoal)
}
