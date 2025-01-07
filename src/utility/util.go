package utility

import (
	"bufio"
	"iter"
	"os"
	"strconv"
	"strings"
)

type base int

const (
	NW base = iota
	N
	NE
	W
	E
	SW
	S
	SE
)

type Move interface {
	Move() base
}

func (b base) Move() base {
	return b
}

func GetMove(m Move) Coordinate {
	switch m {
	case NW:
		return Coordinate{Row: -1, Col: -1}
	case N:
		return Coordinate{Row: -1, Col: 0}
	case NE:
		return Coordinate{Row: -1, Col: 1}
	case W:
		return Coordinate{Row: 0, Col: -1}
	case E:
		return Coordinate{Row: 0, Col: 1}
	case SW:
		return Coordinate{Row: 1, Col: -1}
	case S:
		return Coordinate{Row: 1, Col: 0}
	case SE:
		return Coordinate{Row: 1, Col: 1}
	default:
		panic("Unknown Move")
	}
}

func (t *TransientGrid[T]) iterateDirections(c Coordinate, moves []Move) iter.Seq[Coordinate] {
	return func(yield func(Coordinate) bool) {
		for _, move := range moves {
			mCoord := GetMove(move)
			newCoord := Coordinate{Row: c.Row + mCoord.Row, Col: c.Col + mCoord.Col}
			if newCoord.Col < 0 || newCoord.Col >= t.w || newCoord.Row < 0 || newCoord.Row >= t.h {
				continue
			}
			if !yield(newCoord) {
				return
			}
		}
	}
}

func (t *TransientGrid[T]) IterateFourDirections(c Coordinate) iter.Seq[Coordinate] {
	coords := []Move{N, S, E, W}
	return t.iterateDirections(c, coords)
}

func (t *TransientGrid[T]) IterateEightDirections(c Coordinate) iter.Seq[Coordinate] {
	coords := []Move{N, S, E, W, NW, NE, SW, SE}
	return t.iterateDirections(c, coords)
}

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

type TransientGrid[T any] struct {
	Grid[T]
	transientData []T
}

func MakeTransientGrid[T any](grid *Grid[T]) TransientGrid[T] {
	return TransientGrid[T]{*grid, make([]T, grid.w*grid.h)}
}

func (t *TransientGrid[T]) At(c Coordinate) T {
	return t.Grid.At(c)
}

func (t *TransientGrid[T]) Set(c Coordinate, val T) {
	t.transientData[c.Row*t.h+c.Col] = val
}

func (t *TransientGrid[T]) Update() {
	t.Grid.data = t.transientData
	t.transientData = nil
	t.transientData = make([]T, t.Grid.w*t.Grid.h)
}

func (t *TransientGrid[T]) IterateCoordinates() iter.Seq[Coordinate] {
	return func(yield func(Coordinate) bool) {
		for row := range t.Grid.h {
			for col := range t.Grid.w {
				if !yield(Coordinate{Row: row, Col: col}) {
					return
				}
			}
		}
	}
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

func (g Grid[T]) GetDimensions() Coordinate {
	return Coordinate{Row: g.h, Col: g.w}
}

func ParseBinaryTransientGrid(filePath string, trueRune rune) *TransientGrid[bool] {
	grid := ParseBinaryGrid(filePath, trueRune)
	tGrid := MakeTransientGrid(grid)
	return &tGrid
}

func ParseBinaryGrid(filePath string, trueRune rune) *Grid[bool] {
	lines := ParseLines(filePath)

	grid := MakeGrid[bool](len(lines[0]), len(lines))

	for row, line := range lines {
		for column, val := range line {
			coord := Coordinate{Row: row, Col: column}
			grid.Set(coord, val == trueRune)
		}
	}

	return &grid
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
