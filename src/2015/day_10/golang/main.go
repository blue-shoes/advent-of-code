package main

import (
	"fmt"
	"strconv"

	"github.com/blue-shoes/advent-of-code/utility"
)

func mainPart1(input string) {
	repeats := 40
	tmpInput := input
	for i := 0; i < repeats; i++ {
		nextStr := ""
		runesArr := []rune(tmpInput)
		for j := 0; j < len(runesArr); j++ {
			testRune := runesArr[j]
			num := 1
			for {
				if j+num == len(runesArr) {
					break
				}
				if runesArr[j+num] != testRune {
					break
				}
				num++
			}
			nextStr += strconv.Itoa(num) + string(testRune)
			j += (num - 1)
		}
		tmpInput = nextStr
	}
	fmt.Printf("Length of result is %d\n", len(tmpInput))
}

func main() {
	input := utility.ParseLines("../inputs.txt")[0]

	mainPart1(input)
}
