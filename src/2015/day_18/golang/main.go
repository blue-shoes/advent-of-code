package main

import (
	"fmt"

	"github.com/blue-shoes/advent-of-code/utility"
)

func mainPart1(grid *utility.TransientGrid[bool], seconds int) {
	for range seconds {
		for c := range grid.IterateCoordinates() {
			onCount := 0
			for neighbor := range grid.IterateEightDirections(c) {
				if grid.At(neighbor) {
					onCount++
				}
			}
			if grid.At(c) {
				grid.Set(c, onCount == 2 || onCount == 3)
			} else {
				grid.Set(c, onCount == 3)
			}
		}
		grid.Update()
	}

	onCount := getLightsOn(grid)

	fmt.Printf("After %d seconds, there are %d lights on\n", seconds, onCount)
}

func isCorner(c utility.Coordinate, size utility.Coordinate) bool {
	return (c.Row == 0 || c.Row == size.Row-1) && (c.Col == 0 || c.Col == size.Col-1)
}

func mainPart2(grid *utility.TransientGrid[bool], seconds int) {

	size := grid.Grid.GetDimensions()

	for c := range grid.IterateCoordinates() {
		if isCorner(c, size) {
			grid.Set(c, true)
		} else {
			grid.Set(c, grid.At(c))
		}
	}
	grid.Update()

	for range seconds {
		for c := range grid.IterateCoordinates() {
			if isCorner(c, size) {
				grid.Set(c, true)
				continue
			}
			onCount := 0
			for neighbor := range grid.IterateEightDirections(c) {
				if grid.At(neighbor) {
					onCount++
				}
			}
			if grid.At(c) {
				grid.Set(c, onCount == 2 || onCount == 3)
			} else {
				grid.Set(c, onCount == 3)
			}
		}
		grid.Update()
	}

	onCount := getLightsOn(grid)

	fmt.Printf("After %d seconds, there are %d lights on\n", seconds, onCount)
}

func getLightsOn(grid *utility.TransientGrid[bool]) int {
	onCount := 0
	for c := range grid.IterateCoordinates() {
		if grid.At(c) {
			onCount++
		}
	}
	return onCount
}

func copyGrid(grid *utility.TransientGrid[bool]) *utility.TransientGrid[bool] {
	cGrid := *grid
	return &cGrid
}

func main() {

	grid := utility.ParseBinaryTransientGrid("../inputs.txt", '#')

	gridCopy := copyGrid(grid)

	seconds := 100

	mainPart1(grid, seconds)

	mainPart2(gridCopy, seconds)
}
