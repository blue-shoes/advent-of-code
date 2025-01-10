package main

import (
	"fmt"
	"slices"

	"github.com/blue-shoes/advent-of-code/utility"
	"golang.org/x/exp/maps"
)

func getSubCombinations(subContainers []int, currentCombo []bool, sum, target, currentIdx int) [][]bool {
	allCombos := [][]bool{}
	if len(subContainers) == 1 {
		if sum+subContainers[0] == target {
			cc := make([]bool, len(currentCombo))
			copy(cc, currentCombo)
			cc[currentIdx] = true
			allCombos = append(allCombos, cc)
			return allCombos
		}
		return allCombos
	}

	newSum := sum + subContainers[0]
	if newSum <= target {
		cc := make([]bool, len(currentCombo))
		copy(cc, currentCombo)
		cc[currentIdx] = true
		if newSum == target {
			allCombos = append(allCombos, cc)
		} else {
			allCombos = append(allCombos, getSubCombinations(subContainers[1:], cc, newSum, target, currentIdx+1)...)
		}
	}
	cc := make([]bool, len(currentCombo))
	copy(cc, currentCombo)
	allCombos = append(allCombos, getSubCombinations(subContainers[1:], cc, sum, target, currentIdx+1)...)

	//fmt.Println(len(allCombos))

	return allCombos
}

func subValid(c, c2 []bool) bool {
	for i := range len(c) {
		if c[i] && c2[i] {
			return false
		}
	}
	return true
}

func valid(c []bool, combos [][]bool) bool {
	for _, c2 := range combos {
		if subValid(c, c2) {
			return true
		}
	}
	return false
}

func valid2(c []bool, combos [][]bool) bool {
	for idx, c2 := range combos {
		if subValid(c, c2) {
			for _, c3 := range combos[idx:] {
				if subValid(c, c3) && subValid(c2, c3) {
					return true
				}
			}
		}
	}
	return false
}

func mainPart1(containers []int, totalMass int) {
	target := totalMass / 3
	workSection(containers, target, valid)

}

func mainPart2(containers []int, totalMass int) {
	target := totalMass / 4
	workSection(containers, target, valid2)
}

type fn func([]bool, [][]bool) bool

func workSection(containers []int, target int, valid fn) {
	targetCombos := getSubCombinations(containers, make([]bool, len(containers)), 0, target, 0)

	lengthMap := map[int][][]bool{}

	for _, c := range targetCombos {
		count := 0
		for _, inc := range c {
			if inc {
				count++
			}
		}
		if _, ok := lengthMap[count]; !ok {
			lengthMap[count] = [][]bool{}
		}
		lengthMap[count] = append(lengthMap[count], c)
	}

	keys := maps.Keys(lengthMap)
	slices.Sort(keys)

	minQe := 10000000000000000
	var minCombo []int

	for _, k := range keys {
		for _, c := range lengthMap[k] {
			if valid(c, targetCombos) {
				conts := []int{}
				for idx, inc := range c {
					if inc {
						conts = append(conts, containers[idx])
					}
				}
				qe := utility.Product(conts)
				if qe < minQe {
					minQe = qe
					minCombo = conts
				}
			}
		}
		if minQe < 10000000000000000 {
			break
		}
	}

	fmt.Println("Min length:", keys[0], "Min QE:", minQe, "Combo:", minCombo)

}

func main() {
	lines := utility.ParseLines("../inputs.txt")
	containers := []int{}
	for _, line := range lines {
		containers = append(containers, utility.Atoi(line))
	}

	totalMass := utility.Sum(containers)

	slices.Reverse(containers)

	mainPart1(containers, totalMass)
	mainPart2(containers, totalMass)

}
