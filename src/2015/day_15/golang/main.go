package main

import (
	"fmt"
	"slices"
	"strings"

	"github.com/blue-shoes/advent-of-code/utility"
)

type Ingredient struct {
	name                                            string
	capacity, durability, flavor, texture, calories int
}

func getTotal(ingredients []Ingredient, totals []int) int {
	c := 0
	d := 0
	f := 0
	t := 0
	for idx, ing := range ingredients {
		c += ing.capacity * totals[idx]
		d += ing.durability * totals[idx]
		f += ing.flavor * totals[idx]
		t += ing.texture * totals[idx]
	}
	//fmt.Println(c, d, f, t)
	product := c * d * f * t
	if slices.Min([]int{c, d, f, t}) < 0 {
		if product > 0 {
			product = -product
		}
	}

	return product
}

func testCombo(ingredients []Ingredient, totals []int) bool {
	if utility.Sum(totals) != 100 {
		return false
	}

	calories := 0
	for idx, ing := range ingredients {
		calories += ing.calories * totals[idx]
	}

	return calories == 500
}

func possibleCombos(ingredients []Ingredient) [][]int {
	combos := make([][]int, 0)
	for i := 1; i <= 97; i++ {
		for j := 1; j <= 97-i+1; j++ {
			for k := 1; k < 97-(i+j)+1; k++ {
				test := []int{i, j, k, 100 - i - j - k}
				if testCombo(ingredients, test) {
					combos = append(combos, test)
				}
			}
		}
	}
	return combos
}

func mainPart2(ingredients []Ingredient) {
	combos := possibleCombos(ingredients)

	maxVal := 0
	for _, combo := range combos {
		total := getTotal(ingredients, combo)
		if total > maxVal {
			maxVal = total
		}
	}

	fmt.Printf("Max 500 calorie cookie scores %d.\n", maxVal)

}

func mainPart1(ingredients []Ingredient) {

	//Known positive starting point
	totals := []int{19, 1, 50, 30}

	maxVal := getTotal(ingredients, totals)
	fmt.Println(maxVal, totals)
	for {
		mod := false
		for i := 0; i < len(ingredients); i++ {
			testTotals := make([]int, len(totals))
			copy(testTotals, totals)
			for {
				if testTotals[i] == 100-(len(ingredients)-1) {
					break
				}
				testTotals[i]++
				loopBest := maxVal
				var loopBestJ int
				innerTestTotals := make([]int, len(totals))
				for j := 0; j < len(ingredients); j++ {
					if j == i {
						continue
					}
					if testTotals[j] == 1 {
						continue
					}
					copy(innerTestTotals, testTotals)
					innerTestTotals[j]--
					testVal := getTotal(ingredients, innerTestTotals)
					if testVal >= loopBest || slices.Min(innerTestTotals) <= 0 {
						loopBestJ = j
					}
				}
				testTotals[loopBestJ]--
				testVal := getTotal(ingredients, innerTestTotals)
				if testVal >= maxVal {
					maxVal = testVal
					copy(totals, testTotals)
					mod = true
				} else {
					break
				}

			}
		}
		if !mod {
			break
		}
	}

	getTotal(ingredients, totals)
	fmt.Printf("Max score is %d.\n", maxVal)
}

func main() {
	lines := utility.ParseLines("../inputs.txt")

	ingredients := make([]Ingredient, 0)
	for _, line := range lines {
		noComma := strings.ReplaceAll(line, ",", "")
		split := strings.Split(noComma, " ")
		ints := utility.StringArrayToInts([]string{split[2], split[4], split[6], split[8], split[10]})
		ingredients = append(ingredients, Ingredient{name: split[0], capacity: ints[0], durability: ints[1], flavor: ints[2], texture: ints[3], calories: ints[4]})
		fmt.Println(ints)
	}

	mainPart1(ingredients)
	mainPart2(ingredients)

}
