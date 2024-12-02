package main

import (
	_ "embed"
	"math"
	"regexp"
	"sort"
	"strconv"
)

//go:embed inputs.txt
var inputs string

func parseLists() (list1 []int, list2 []int) {
	re := regexp.MustCompile("\\s+|\n")
	split := re.Split(inputs, -1)

	list1 = make([]int, len(split)/2)
	list2 = make([]int, len(split)/2)

	for i := 0; i < len(split); i++ {
		val, _ := strconv.Atoi(split[i])
		if i%2 == 0 {
			list1 = append(list1, val)
		} else {
			list2 = append(list2, val)
		}
	}

	sort.Ints(list1)
	sort.Ints(list2)

	return list1, list2
}

func main_part2() {
	list1, list2 := parseLists()

	countMap := make(map[int]int)
	for _, val2 := range list2 {
		countMap[val2]++
	}

	sim_score := 0
	for _, val1 := range list1 {
		sim_score += val1 * countMap[val1]
	}

	println("sim_score = " + strconv.Itoa(sim_score))
}

func main_part1() {
	list1, list2 := parseLists()

	diff_sum := 0
	for idx, val1 := range list1 {
		diff_sum += int(math.Abs(float64(val1 - list2[idx])))
	}

	println("diff_sum = " + strconv.Itoa(diff_sum))

}

func main() {
	main_part1()
	main_part2()
}
