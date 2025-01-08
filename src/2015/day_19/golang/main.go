package main

import (
	"fmt"
	"regexp"
	"strings"

	"github.com/blue-shoes/advent-of-code/utility"
)

var instructions [][]string

func mainPart1(inputString string) {
	outputs := make([]string, 0)
	for _, i := range instructions {
		idx := 0
		for {
			if strings.Contains(inputString[idx:], i[0]) {
				output := inputString[:idx] + strings.Replace(inputString[idx:], i[0], i[1], 1)
				outputs = append(outputs, output)
				idx = idx + strings.Index(inputString[idx:], i[0]) + 1
			} else {
				break
			}
		}
	}

	unique := utility.RemoveDuplicates(outputs)
	fmt.Printf("There are %d unique molecules created.\n", len(unique))
}

func mainPart2(endString string) {
	r1 := regexp.MustCompile(`[A-Z][a-z]?`)

	noYMatch := regexp.MustCompile(`[A-Z][a-z]?Rn([^RY]+?)Ar`)
	oneYMatch := regexp.MustCompile(`[A-Z][a-z]?Rn([^RY]+?)Y([^RY]+?)Ar`)
	twoYMatch := regexp.MustCompile(`[A-Z][a-z]?Rn([^RY]+?)Y([^RY]+?)Y([^RY]+?)Ar`)

	count := 0
	for {
		if strings.Count(endString, "Rn") == 0 {
			break
		}
		smallMatch := noYMatch.FindAllStringSubmatch(endString, -1)
		for _, sm := range smallMatch {
			subTokens := r1.FindAllString(sm[1], -1)
			count += (len(subTokens))
			endString = strings.Replace(endString, sm[0], "X", 1)
		}

		medMatch := oneYMatch.FindAllStringSubmatch(endString, -1)
		for _, mm := range medMatch {
			subTokens := r1.FindAllString(mm[1], -1)
			count += (len(subTokens))
			subTokens = r1.FindAllString(mm[2], -1)
			count += len(subTokens) - 1
			endString = strings.Replace(endString, mm[0], "X", 1)
		}

		lgMatch := twoYMatch.FindAllStringSubmatch(endString, -1)
		for _, lm := range lgMatch {
			subTokens := r1.FindAllString(lm[1], -1)
			count += (len(subTokens))
			subTokens = r1.FindAllString(lm[2], -1)
			count += len(subTokens) - 1
			subTokens = r1.FindAllString(lm[3], -1)
			count += len(subTokens) - 1
			endString = strings.Replace(endString, lm[0], "X", 1)
		}
	}

	newElementCount := len(r1.FindAllString(endString, -1))

	count += newElementCount - 1

	fmt.Printf("There minimum moves to get the medicine is %d.\n", count)

}

func main() {
	lines := utility.ParseLines("../inputs.txt")
	instructions = make([][]string, 0)
	endInstructions := false
	var inputString string
	for _, line := range lines {
		if len(strings.TrimSpace(line)) == 0 {
			endInstructions = true
			continue
		}
		if endInstructions {
			inputString = strings.TrimSpace(line)
		} else {
			instructions = append(instructions, strings.Split(line, " => "))
		}
	}

	mainPart1(inputString)
	mainPart2(inputString)
}
