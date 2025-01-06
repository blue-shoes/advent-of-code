package main

import (
	"fmt"
	"strconv"
	"strings"

	"golang.org/x/exp/maps"

	"github.com/blue-shoes/advent-of-code/utility"
)

func getMaxHappiness(partners map[string]map[string]int, combos [][]string) int {
	maxHappiness := 0
	for _, combo := range combos {
		testHappiness := 0
		for i := 0; i < len(combo)-1; i++ {

			if i == 0 {
				p1 := combo[i]
				p2 := combo[len(combo)-1]
				testHappiness += partners[p1][p2]
				testHappiness += partners[p2][p1]
			}

			p1 := combo[i]
			p2 := combo[i+1]
			testHappiness += partners[p1][p2]
			testHappiness += partners[p2][p1]

		}
		if testHappiness > maxHappiness {
			maxHappiness = testHappiness
		}
	}

	return maxHappiness
}

func mainPart1(partners map[string]map[string]int) {
	combos := utility.GeneratePermutationsRecursive(maps.Keys(partners))

	maxHappiness := getMaxHappiness(partners, combos)

	fmt.Printf("Optimal happiness if %d.\n", maxHappiness)
}

func mainPart2(partners map[string]map[string]int) {
	partners["Me"] = make(map[string]int)
	for k, v := range partners {
		if k == "Me" {
			continue
		}
		v["Me"] = 0
		partners["Me"][k] = 0
	}

	combos := utility.GeneratePermutationsRecursive(maps.Keys(partners))
	maxHappiness := getMaxHappiness(partners, combos)
	fmt.Printf("New Optimal happiness is %d.\n", maxHappiness)
}

func main() {
	lines := utility.ParseLines("../inputs.txt")

	twoWayPartners := make(map[string]map[string]int)

	for _, line := range lines {
		split := strings.Split(line, " ")
		happiness, _ := strconv.Atoi(split[3])
		if split[2] == "lose" {
			happiness = -happiness
		}
		if _, exists := twoWayPartners[split[0]]; !exists {
			twoWayPartners[split[0]] = make(map[string]int)
		}
		p_name := split[len(split)-1]
		p_name = p_name[:len(p_name)-1]
		twoWayPartners[split[0]][p_name] = happiness
	}

	mainPart1(twoWayPartners)
	mainPart2(twoWayPartners)

}
