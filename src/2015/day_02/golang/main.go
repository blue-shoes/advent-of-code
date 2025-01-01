package main

import (
	"fmt"
	"slices"

	"github.com/blue-shoes/advent-of-code/utility"
)

func GetSideAreas(dims []int) []int {
	side1 := dims[0] * dims[1]
	side2 := dims[1] * dims[2]
	side3 := dims[0] * dims[2]

	return []int{side1, side2, side3}
}

func GetSidePerimeters(dims []int) []int {
	side1 := 2 * (dims[0] + dims[1])
	side2 := 2 * (dims[1] + dims[2])
	side3 := 2 * (dims[0] + dims[2])

	return []int{side1, side2, side3}
}

func main_part1(lines [][]int) {
	totalArea := 0
	for _, dims := range lines {
		sideAreas := GetSideAreas(dims)
		minSide := slices.Min(sideAreas)

		neededArea := minSide + 2*utility.Sum(sideAreas)
		totalArea += neededArea
	}
	fmt.Printf("Need a total of %d square feet.\n", totalArea)
}

func main_part2(lines [][]int) {
	totalLength := 0
	for _, dims := range lines {
		perims := GetSidePerimeters(dims)
		minPerim := slices.Min(perims)
		volume := utility.Product(dims)
		totalLength += minPerim + volume
	}
	fmt.Printf("Need a total of %d feet of ribbon.\n", totalLength)
}

func main() {
	lines := utility.ParseIntArrays("../inputs.txt", "x")
	main_part1(lines)
	main_part2(lines)
}
