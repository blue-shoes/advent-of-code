package main

import (
	"fmt"
	"math"
	"regexp"
	"strings"

	"github.com/blue-shoes/advent-of-code/utility"
)

type base int

const (
	ON base = iota
	OFF
	TOGGLE
)

type Action struct {
	startCoord utility.Coordinate
	endCoord   utility.Coordinate
	action     base
}

func applyAction(grid *utility.Grid[bool], action Action) {
	for r := action.startCoord.Row; r <= action.endCoord.Row; r++ {
		for c := action.startCoord.Col; c <= action.endCoord.Col; c++ {
			coord := utility.Coordinate{Row: r, Col: c}
			if action.action == ON {
				grid.Set(coord, true)
			} else if action.action == OFF {
				grid.Set(coord, false)
			} else {
				grid.Set(coord, !grid.At(coord))
			}
		}
	}
}

func getTotalOn(grid *utility.Grid[bool]) int {
	count := 0
	for _, d := range grid.GetData() {
		if d {
			count++
		}
	}
	return count
}

func mainPart1(actions []Action) {
	grid := utility.MakeGrid[bool](1000, 1000)
	for _, action := range actions {
		applyAction(&grid, action)
	}
	totalOn := getTotalOn(&grid)
	fmt.Printf("There are %d total lights on.\n", totalOn)
}

func applyElvishAction(grid *utility.Grid[int], action Action) {
	for r := action.startCoord.Row; r <= action.endCoord.Row; r++ {
		for c := action.startCoord.Col; c <= action.endCoord.Col; c++ {
			coord := utility.Coordinate{Row: r, Col: c}
			if action.action == ON {
				grid.Set(coord, grid.At(coord)+1)
			} else if action.action == OFF {
				grid.Set(coord, int(math.Max(float64(grid.At(coord)-1), 0)))
			} else {
				grid.Set(coord, grid.At(coord)+2)
			}
		}
	}
}

func getTotalBrightness(grid *utility.Grid[int]) int {
	brightness := 0
	for _, d := range grid.GetData() {
		brightness += d
	}
	return brightness
}

func mainPart2(actions []Action) {
	grid := utility.MakeGrid[int](1000, 1000)
	for _, action := range actions {
		applyElvishAction(&grid, action)
	}
	totalBrightness := getTotalBrightness(&grid)
	fmt.Printf("The total bightness is %d.\n", totalBrightness)
}

func main() {
	lines := utility.ParseLines("../inputs.txt")
	actions := make([]Action, 0)
	for _, line := range lines {
		var action base
		if strings.HasPrefix(line, "turn on") {
			action = ON
		} else if strings.HasPrefix(line, "turn off") {
			action = OFF
		} else {
			action = TOGGLE
		}
		r1, _ := regexp.Compile(`(\d+,\d+)`)
		matches := r1.FindAllString(line, -1)
		c := utility.StringArrayToInts(strings.Split(matches[0], ","))
		s := utility.Coordinate{Row: c[0], Col: c[1]}
		c = utility.StringArrayToInts(strings.Split(matches[1], ","))
		e := utility.Coordinate{Row: c[0], Col: c[1]}
		actions = append(actions, Action{startCoord: s, endCoord: e, action: action})
	}

	mainPart1(actions)
	mainPart2(actions)
}
