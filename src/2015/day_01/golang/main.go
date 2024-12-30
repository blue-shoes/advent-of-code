package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func main_part1(lines []string) {
	openCount := 0
	closeCount := 0
	for _, line := range lines {
		openCount = openCount + strings.Count(line, "(")
		closeCount = closeCount + strings.Count(line, ")")
	}
	newFloor := openCount - closeCount
	fmt.Printf("The new floor is %d \n", newFloor)
}

func main_part2(lines []string) {
	openCount := 0
	closeCount := 0
	for _, line := range lines {
		for idx, char := range line {
			if char == '(' {
				openCount += 1
			} else {
				closeCount += 1
			}
			if closeCount > openCount {
				fmt.Printf("First time in the basement is position %d\n", idx+1)
				return
			}
		}
	}
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
