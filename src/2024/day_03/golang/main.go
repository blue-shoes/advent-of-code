package main

import (
	_ "embed"
	"regexp"
	"strconv"
	"strings"
)

//go:embed inputs.txt
var inputs string

var regexPattern = regexp.MustCompile("mul\\((\\d{1,3},\\d{1,3})\\)")

func getSum(valStr string) int {
	multParses := regexPattern.FindAllStringSubmatch(valStr, -1)
	multList := make([][]int, len(multParses))
	for i := range multParses {
		multLine := strings.Split(multParses[i][1], ",")
		v1, _ := strconv.Atoi(multLine[0])
		v2, _ := strconv.Atoi(multLine[1])
		multList[i] = []int{v1, v2}
	}

	return reduce(multList, func(acc int, b []int) int { return acc + (b[0] * b[1]) }, 0)
}

func mainPart1() {
	sum := getSum(inputs)
	println("Multiplication results are", strconv.Itoa(sum))

}

func mainPart2() {
	dontSplit := strings.Split(inputs, "don't()")

	doSplits := make([]string, 0)
	for idx, val := range dontSplit {
		if idx == 0 {
			doSplits = append(doSplits, val)
			continue
		}
		doSplit := strings.Split(val, "do()")
		doSplits = append(doSplits, doSplit[1:]...)
	}

	sum := getSum(strings.Join(doSplits, ""))
	println("Enabled multiplication results are", strconv.Itoa(sum))

}

func reduce[T, M any](s []T, f func(M, T) M, initValue M) M {
	acc := initValue
	for _, val := range s {
		acc = f(acc, val)
	}
	return acc
}

func main() {
	mainPart1()
	mainPart2()
}
