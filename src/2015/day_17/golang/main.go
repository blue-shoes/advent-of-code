package main

import (
	"fmt"
	"slices"
	"strconv"
	"strings"

	"github.com/blue-shoes/advent-of-code/utility"
	"golang.org/x/exp/maps"
)

func recursiveSearch(sizes []int, remainingLiters int) int {
	combos := 0
	newRemainingLiters := remainingLiters - sizes[0]
	if newRemainingLiters == 0 {
		combos++
		return combos
	}
	for idx, size := range sizes[1:] {
		if size <= newRemainingLiters {
			combos += recursiveSearch(sizes[1+idx:], newRemainingLiters)
		}

	}

	return combos
}

func mainPart1(sizes []int, totalLiters int) {

	uniqueCombos := 0
	for idx := range sizes {
		uniqueCombos += recursiveSearch(sizes[idx:], totalLiters)
	}

	fmt.Printf("There are a total of %d ways to store %d liters.\n", uniqueCombos, totalLiters)

}

func recursiveSearchMin(sizes []int, remainingLiters int, currentCombo []int, uniqueCombos map[int]int) {
	newRemainingLiters := remainingLiters - sizes[0]

	if newRemainingLiters == 0 {
		uniqueCombos[len(currentCombo)]++
		return
	}
	for idx, size := range sizes[1:] {
		if size <= newRemainingLiters {
			newCombo := make([]int, len(currentCombo))
			copy(newCombo, currentCombo)
			newCombo = append(newCombo, size)
			recursiveSearchMin(sizes[1+idx:], newRemainingLiters, newCombo, uniqueCombos)
		}

	}
}

func mainPart2(sizes []int, totalLiters int) {
	uniqueCombos := make(map[int]int)
	for idx, size := range sizes {
		currentCombo := make([]int, 0)
		currentCombo = append(currentCombo, size)
		recursiveSearchMin(sizes[idx:], totalLiters, currentCombo, uniqueCombos)
	}

	minKey := slices.Min(maps.Keys(uniqueCombos))

	fmt.Printf("There are a total of %d ways to store %d liters in %d containers.\n", uniqueCombos[minKey], totalLiters, minKey)
}

func main() {
	containerSizeLines := utility.ParseLines("../inputs.txt")
	totalLiters := 150

	sizes := make([]int, 0)
	for _, line := range containerSizeLines {
		size, _ := strconv.Atoi(strings.TrimSpace(line))
		sizes = append(sizes, size)
	}

	mainPart1(sizes, totalLiters)
	mainPart2(sizes, totalLiters)
}
