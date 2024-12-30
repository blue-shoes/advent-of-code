package main

import (
	"bufio"
	"fmt"
	"os"
	"slices"
	"strconv"
	"strings"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func StringArrayToInts(StrArray []string) []int {
	t := make([]int, len(StrArray))
	for idx, str := range StrArray {
		val, err := strconv.Atoi(str)
		check(err)
		t[idx] = val
	}
	return t
}

func reduce[T, M any](s []T, f func(M, T) M, initValue M) M {
	acc := initValue
	for _, val := range s {
		acc = f(acc, val)
	}
	return acc
}

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

func main_part1(lines []string) {
	totalArea := 0
	for _, present := range lines {
		dims := StringArrayToInts(strings.Split(present, "x"))
		sideAreas := GetSideAreas(dims)
		minSide := slices.Min(sideAreas)

		neededArea := minSide + 2*(reduce(sideAreas, func(acc int, b int) int { return acc + b }, 0))
		totalArea += neededArea
	}
	fmt.Printf("Need a total of %d square feet.\n", totalArea)
}

func main_part2(lines []string) {
	totalLength := 0
	for _, present := range lines {
		dims := StringArrayToInts(strings.Split(present, "x"))
		perims := GetSidePerimeters(dims)
		minPerim := slices.Min(perims)
		volume := reduce(dims, func(acc int, b int) int { return acc * b }, 1)
		totalLength += minPerim + volume
	}
	fmt.Printf("Need a total of %d feet of ribbon.\n", totalLength)
}

func main() {
	file, err := os.Open("../inputs.txt")
	check(err)
	defer file.Close()

	lines := make([]string, 0)

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	main_part1(lines)
	main_part2(lines)
}
