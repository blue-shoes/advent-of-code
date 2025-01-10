package main

import (
	"fmt"

	"github.com/blue-shoes/advent-of-code/utility"
)

func nextCode(current int) int {
	return (current * 252533) % 33554393
}

func mainPart1(coord utility.Coordinate) {
	firstCode := 20151125

	row1Col := coord.Col + coord.Row - 1

	sum := 0
	for i := range row1Col {
		sum += i
	}

	targetCode := sum + row1Col - coord.Row

	code := firstCode
	for range targetCode {
		code = nextCode(code)
	}

	fmt.Printf("Enter code %d.\n", code)

}

func main() {
	codeCoord := utility.Coordinate{Row: 3010, Col: 3019}

	mainPart1(codeCoord)

}
