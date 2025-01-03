package main

import (
	"fmt"
	"regexp"
	"strconv"

	"github.com/blue-shoes/advent-of-code/utility"
	"golang.org/x/exp/maps"
)

type Trip struct {
	loc  string
	dist int
}

func generatePermutationsRecursive(keys []string) [][]string {
	if len(keys) == 0 {
		return [][]string{}
	}
	if len(keys) == 1 {
		return [][]string{{keys[0]}}
	}
	permutations := [][]string{}

	for i, key := range keys {
		remaining := make([]string, len(keys)-1)
		copy(remaining[:i], keys[:i])
		copy(remaining[i:], keys[i+1:])

		subpermutations := generatePermutationsRecursive(remaining)

		for _, p := range subpermutations {
			permutations = append(permutations, append([]string{key}, p...))
		}
	}

	return permutations
}

func mainPart2(outbounds map[string]map[string]int) {
	keys := maps.Keys(outbounds)
	maxDist := 0
	for _, perm := range generatePermutationsRecursive(keys) {
		dist := 0
		for i := 0; i < len(perm)-1; i++ {
			dist += outbounds[perm[i]][perm[i+1]]
		}
		if dist > maxDist {
			maxDist = dist
		}
	}
	fmt.Printf("The maximum distance is %d\n", maxDist)
}

func mainPart1(outbounds map[string]map[string]int) {
	keys := maps.Keys(outbounds)
	minDist := 100000
	for _, perm := range generatePermutationsRecursive(keys) {
		dist := 0
		for i := 0; i < len(perm)-1; i++ {
			dist += outbounds[perm[i]][perm[i+1]]
		}
		if dist < minDist {
			minDist = dist
		}
	}
	fmt.Printf("The minimum distance is %d\n", minDist)
}

func main() {
	lines := utility.ParseLines("../inputs.txt")

	outbounds := make(map[string]map[string]int)
	r1 := regexp.MustCompile(`(\w+) to (\w+) = (\d+)`)
	for _, line := range lines {
		match := r1.FindAllStringSubmatch(line, -1)
		dist, _ := strconv.Atoi(match[0][3])
		//trip := Trip{loc: match[0][2], dist: dist}
		if _, present := outbounds[match[0][1]]; !present {
			outbounds[match[0][1]] = make(map[string]int)
		}
		outbounds[match[0][1]][match[0][2]] = dist
		//if inp1, present := outbounds[match[0][1]]; present {

		//} else {
		//	outbounds[match[0][1]] = append(make([]Trip, 0), trip)
		//}
		//trip = Trip{loc: match[0][1], dist: dist}
		//if inp2, present := outbounds[match[0][2]]; present {
		if _, present := outbounds[match[0][2]]; !present {
			outbounds[match[0][2]] = make(map[string]int)
		}
		outbounds[match[0][2]][match[0][1]] = dist
		//} else {
		//	outbounds[match[0][2]] = append(make([]Trip, 0), trip)
		//}
	}

	mainPart1(outbounds)
	mainPart2(outbounds)
}
