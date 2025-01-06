package main

import (
	"fmt"
	"math"
	"slices"
	"strings"

	"github.com/blue-shoes/advent-of-code/utility"
)

type Reindeer struct {
	speed, flyTime, restTime int
	name                     string
}

func mainPart2(reindeer []Reindeer) {
	totalTime := 2503

	points := make([]int, len(reindeer))

	for s := 1; s <= totalTime; s++ {
		maxDist := 0
		maxIdx := make([]int, 0)
		for idx, deer := range reindeer {
			cycleTime := deer.flyTime + deer.restTime
			cycles := s / cycleTime
			additionalFlyTime := int(math.Min(float64(s%cycleTime), float64(deer.flyTime)))
			dist := (cycles*deer.flyTime + additionalFlyTime) * deer.speed

			if dist > maxDist {
				maxDist = dist
				maxIdx = []int{idx}
			} else if dist == maxDist {
				maxIdx = append(maxIdx, idx)
			}
		}
		for _, idx := range maxIdx {
			points[idx]++
		}
	}
	//fmt.Println(points)
	fmt.Printf("Max points is %d.\n", slices.Max(points))
}

func mainPart1(reindeer []Reindeer) {
	maxDist := 0
	totalTime := 2503

	for _, deer := range reindeer {
		cycleTime := deer.flyTime + deer.restTime
		cycles := totalTime / cycleTime
		additionalFlyTime := int(math.Min(float64(totalTime%cycleTime), float64(deer.flyTime)))
		dist := (cycles*deer.flyTime + additionalFlyTime) * deer.speed

		if dist > maxDist {
			maxDist = dist
		}
	}

	fmt.Printf("Max distance flown is %d.\n", maxDist)
}

func main() {
	lines := utility.ParseLines("../inputs.txt")

	reindeer := make([]Reindeer, 0)
	for _, line := range lines {
		split := strings.Split(line, " ")
		ints := utility.StringArrayToInts([]string{split[3], split[6], split[13]})
		reindeer = append(reindeer, Reindeer{speed: ints[0], flyTime: ints[1], restTime: ints[2], name: split[0]})
	}

	mainPart1(reindeer)
	mainPart2(reindeer)
}
