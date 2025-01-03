package main

import (
	"fmt"
	"strconv"
	"strings"

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
		fmt.Println(tmpInput)
	}
	fmt.Printf("Length of result is %d\n", len(tmpInput))
}

type Atom struct {
	val   string
	len   int
	decay []string
}

func getAtomicsMap() map[string]Atom {
	//atomic.txt is a text file of the https://en.wikipedia.org/wiki/Look-and-say_sequence#Cosmological_decay table
	atomicLines := utility.ParseLines("../atomic.txt")
	atoms := make(map[string]Atom)
	for _, line := range atomicLines {
		array := strings.Split(line, " ")
		decay := strings.Split(strings.TrimSpace(array[3]), ".")
		val := strings.TrimSpace(array[2])
		atoms[strings.TrimSpace(array[1])] = Atom{val: val, len: len(val), decay: decay}
	}
	return atoms
}

func mainPart2(input string, atomics map[string]Atom) {
	repeats := 50
	var initAtom string
	for k, v := range atomics {
		if v.val == input {
			initAtom = k
			break
		}
	}
	atomCount := make(map[string]int)
	atomCount[initAtom] = 1
	for i := 0; i < repeats; i++ {
		nextCount := make(map[string]int)
		for k, v := range atomCount {
			for _, a := range atomics[k].decay {
				if count, present := nextCount[a]; present {
					nextCount[a] = count + v
				} else {
					nextCount[a] = v
				}
			}
		}
		atomCount = nextCount
	}

	totalLength := 0
	for k, v := range atomCount {
		totalLength += v * atomics[k].len
	}
	fmt.Printf("Total length is %d\n", totalLength)
}

func main() {
	input := utility.ParseLines("../inputs.txt")[0]

	atomics := getAtomicsMap()

	mainPart1(input)
	mainPart2(input, atomics)
}
