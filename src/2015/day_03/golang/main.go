package main

import (
	"fmt"

	"github.com/blue-shoes/advent-of-code/utility"
)

func mainPart2(moves string) {
	visited := make([]utility.Coordinate, 0)
	current1 := utility.Coordinate{Row: 0, Col: 0}
	current2 := utility.Coordinate{Row: 0, Col: 0}
	visited = append(visited, current1)
	for idx, direction := range moves {
		var moveCoord utility.Coordinate
		if idx%2 == 0 {
			moveCoord = current1
		} else {
			moveCoord = current2
		}
		if direction == '^' {
			moveCoord = utility.Coordinate{Row: moveCoord.Row - 1, Col: moveCoord.Col}
		} else if direction == '>' {
			moveCoord = utility.Coordinate{Row: moveCoord.Row, Col: moveCoord.Col + 1}
		} else if direction == 'v' {
			moveCoord = utility.Coordinate{Row: moveCoord.Row + 1, Col: moveCoord.Col}
		} else if direction == '<' {
			moveCoord = utility.Coordinate{Row: moveCoord.Row, Col: moveCoord.Col - 1}
		}
		visited = append(visited, moveCoord)
		if idx%2 == 0 {
			current1 = moveCoord
		} else {
			current2 = moveCoord
		}
	}
	uniqueHouses := utility.RemoveDuplicates(visited)

	fmt.Printf("There were %d unique houses visited with RoboSanta.\n", len(uniqueHouses))
}

func mainPart1(moves string) {
	visited := make([]utility.Coordinate, 0)
	current := utility.Coordinate{Row: 0, Col: 0}
	visited = append(visited, current)
	for _, direction := range moves {
		if direction == '^' {
			current = utility.Coordinate{Row: current.Row - 1, Col: current.Col}
		} else if direction == '>' {
			current = utility.Coordinate{Row: current.Row, Col: current.Col + 1}
		} else if direction == 'v' {
			current = utility.Coordinate{Row: current.Row + 1, Col: current.Col}
		} else if direction == '<' {
			current = utility.Coordinate{Row: current.Row, Col: current.Col - 1}
		}
		visited = append(visited, current)
	}
	uniqueHouses := utility.RemoveDuplicates(visited)

	fmt.Printf("There were %d unique houses visited.\n", len(uniqueHouses))
}

func main() {

	moves := utility.ParseLines("../inputs.txt")[0]

	mainPart1(moves)
	mainPart2(moves)
}
