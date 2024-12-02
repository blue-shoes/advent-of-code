package main

import (
	_ "embed"
	"math"
	"strconv"
	"strings"
)

//go:embed inputs.txt
var inputs string

func evaluateReport(report []int) (bool, int) {
	lastVal := math.MaxInt64
	lastInc := math.MaxInt64
	for idx, level := range report {
		if lastVal == math.MaxInt64 {
			lastVal = level
			continue
		}
		inc := lastVal - level
		lastVal = level
		if math.Abs(float64(inc)) > 3 {
			return false, idx
		}
		if lastInc == math.MaxInt64 {
			lastInc = inc
			continue
		}
		if inc*lastInc <= 0 {
			return false, idx
		}
		lastInc = inc
	}
	return true, -1
}

func mainPart1(reports [][]int) {
	safe_count := 0
	for _, report := range reports {
		safe, _ := evaluateReport(report)
		if safe {
			safe_count++
		}
	}
	println("There are", strconv.Itoa(safe_count), "safe reports")
}

func mainPart2(reports [][]int) {
	safeCount := 0

	for _, report := range reports {
		safe, idx := evaluateReport(report)
		if safe {
			safeCount++
			continue
		}
		safe, _ = evaluateReport(removeItem(report, idx))
		if safe {
			safeCount++
			continue
		}
		safe, _ = evaluateReport(removeItem(report, idx-1))
		if safe {
			safeCount++
			continue
		}

		if idx == 2 {
			safe, _ = evaluateReport(removeItem(report, 0))
			if safe {
				safeCount++
			}
		}

	}
	println("There are", strconv.Itoa(safeCount), "safe reports with Problem Dampener")
}

func removeItem(s []int, idx int) []int {
	removedIndex := make([]int, 0)
	removedIndex = append(removedIndex, s[:idx]...)
	return append(removedIndex, s[idx+1:]...)
}

func main() {
	reportLines := strings.Split(inputs, "\n")
	reports := make([][]int, 0)

	for _, reportLine := range reportLines {
		strSlice := strings.Split(reportLine, " ")
		intSlice := make([]int, len(strSlice))
		for idx, val := range strSlice {
			intSlice[idx], _ = strconv.Atoi(val)
		}
		reports = append(reports, intSlice)
	}

	mainPart1(reports)
	mainPart2(reports)
}
