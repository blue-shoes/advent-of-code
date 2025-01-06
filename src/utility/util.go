package utility

import (
	"bufio"
	"os"
	"strconv"
	"strings"
)

type Coordinate struct {
	Row, Col int
}

type TwoDMap struct {
	startCoord, endCoord Coordinate
	walls                []Coordinate
}

type ParseRunes struct {
	startRune, endRune, wallRune rune
}

func Check(e error) {
	if e != nil {
		panic(e)
	}
}

type Grid[T any] struct {
	w, h int
	data []T
}

func MakeGrid[T any](w, h int) Grid[T] {
	return Grid[T]{w, h, make([]T, w*h)}
}
func (g Grid[T]) At(c Coordinate) T {
	return g.data[c.Row*g.h+c.Col]
}
func (g Grid[T]) Set(c Coordinate, val T) {
	g.data[c.Row*g.h+c.Col] = val
}
func (g Grid[T]) GetData() []T {
	return g.data
}

func ParseTwoDMap(filepath string, parseRunes ParseRunes) *TwoDMap {
	lines := ParseLines(filepath)
	walls := make([]Coordinate, 0)
	var startPos Coordinate
	var endPos Coordinate
	for row, line := range lines {
		for column, val := range line {
			if val == parseRunes.startRune {
				startPos = Coordinate{row, column}
			}
			if val == parseRunes.endRune {
				endPos = Coordinate{row, column}
			}
			if val == parseRunes.wallRune {
				walls = append(walls, Coordinate{row, column})
			}
		}
	}
	return &TwoDMap{startPos, endPos, walls}
}

func ParseIntArrays(filePath string, separator string) [][]int {
	lines := ParseLines(filePath)
	returnArray := make([][]int, 0)
	for _, line := range lines {

		returnArray = append(returnArray, StringArrayToInts(strings.Split(line, separator)))
	}
	return returnArray
}

func ParseLines(filePath string) []string {
	file, err := os.Open(filePath)
	Check(err)
	defer file.Close()

	lines := make([]string, 0)

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	return lines
}

func StringArrayToInts(StrArray []string) []int {
	t := make([]int, len(StrArray))
	for idx, str := range StrArray {
		val, err := strconv.Atoi(str)
		Check(err)
		t[idx] = val
	}
	return t
}

func Reduce[T, M any](s []T, f func(M, T) M, initValue M) M {
	acc := initValue
	for _, val := range s {
		acc = f(acc, val)
	}
	return acc
}

func Sum(s []int) int {
	return Reduce(s, func(acc int, b int) int { return acc + b }, 0)
}

func Product(s []int) int {
	return Reduce(s, func(acc int, b int) int { return acc * b }, 1)
}

func RemoveDuplicates[T comparable](sliceList []T) []T {
	allKeys := make(map[T]bool)
	list := []T{}
	for _, item := range sliceList {
		if _, value := allKeys[item]; !value {
			allKeys[item] = true
			list = append(list, item)
		}
	}
	return list
}

func GeneratePermutationsRecursive(keys []string) [][]string {
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

		subpermutations := GeneratePermutationsRecursive(remaining)

		for _, p := range subpermutations {
			permutations = append(permutations, append([]string{key}, p...))
		}
	}

	return permutations
}
