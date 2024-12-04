package main

import (
	_ "embed"
	"strconv"
	"strings"
)

//go:embed inputs.txt
var input string

func searchDirection(text [][]string, start_x int, start_y int, dir int, matchLen int, matchStr string) (bool, []int) {
	var next []int
	switch dir {
	case 1:
		next = []int{-1, -1}
	case 2:
		next = []int{0, -1}
	case 3:
		next = []int{1, -1}
	case 4:
		next = []int{1, 0}
	case 5:
		next = []int{1, 1}
	case 6:
		next = []int{0, 1}
	case 7:
		next = []int{-1, 1}
	case 8:
		next = []int{-1, 0}
	}

	max_x := start_x + matchLen*next[0]
	max_y := start_y + matchLen*next[1]

	if max_y < 0 || max_x < 0 || max_y >= len(text) || max_x >= len(text[start_y]) {
		return false, []int{-1, -1}
	}

	for idx := range matchLen {
		if text[start_y+next[1]*(idx+1)][start_x+next[0]*(idx+1)] != strings.Split(matchStr, "")[idx] {
			return false, []int{-1, -1}
		}
	}

	return true, []int{start_x + next[0]*(matchLen-1), start_y + next[1]*(matchLen-1)}
}

func mainPart1(text [][]string) {
	count := 0
	for idx_y, line := range text {
		for idx_x, char := range line {
			if char == "X" {
				for _, dir := range []int{1, 2, 3, 4, 5, 6, 7, 8} {
					match, _ := searchDirection(text, idx_x, idx_y, dir, 3, "MAS")
					if match {
						count++
					}
				}
			}
		}
	}
	println("XMAS appears", strconv.Itoa(count), "times")
}

type coords struct {
	x, y int
}

func mainPart2(text [][]string) {
	aLocations := map[coords]bool{}
	count := 0

	for idx_y, line := range text {
		for idx_x, char := range line {
			if char == "M" {
				for _, dir := range []int{1, 3, 5, 7} {
					match, m_coords := searchDirection(text, idx_x, idx_y, dir, 2, "AS")
					if match {
						coord := coords{m_coords[0], m_coords[1]}
						if aLocations[coord] {
							count++
						} else {
							aLocations[coord] = true
						}
					}
				}
			}
		}
	}
	println("X-MAS appears", strconv.Itoa(count), "times")
}

func main() {
	wordSearchLines := strings.Split(input, "\n")
	wordSearch := make([][]string, len(wordSearchLines))
	for idx, line := range wordSearchLines {
		wordSearch[idx] = strings.Split(line, "")
	}
	mainPart1(wordSearch)
	mainPart2(wordSearch)
}
