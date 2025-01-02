package main

import (
	"fmt"
	"regexp"
	"strings"

	"github.com/blue-shoes/advent-of-code/utility"
)

func mainPart1(lines []string) {
	totalLiteral := 0
	totalValue := 0

	for _, line := range lines {
		totalLiteral += len(line)
		tmp := strings.ReplaceAll(line, `\\`, `|`)
		tmp = strings.ReplaceAll(tmp, `\"`, `"`)
		asciiMatch := regexp.MustCompile(`\\x(\S\S)`)
		asciiCount := len(asciiMatch.FindAllStringSubmatch(tmp, -1))
		totalValue += len(tmp) - (asciiCount * 3) - 2
	}

	fmt.Printf("%d total. %d value. Difference: %d\n", totalLiteral, totalValue, totalLiteral-totalValue)
}

func mainPart2(lines []string) {
	totalLiteral := 0
	totalNewLiteral := 0

	for _, line := range lines {
		totalLiteral += len(line)
		tmp := strings.ReplaceAll(line, `\`, `\\`)
		tmp = strings.ReplaceAll(tmp, `"`, `\"`)
		totalNewLiteral += len(tmp) + 2
	}
	fmt.Printf("%d total. %d value. Difference: %d\n", totalLiteral, totalNewLiteral, totalNewLiteral-totalLiteral)
}

func main() {
	lines := utility.ParseLines("../inputs.txt")

	mainPart1(lines)
	mainPart2(lines)
}
