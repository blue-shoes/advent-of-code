package main

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/blue-shoes/advent-of-code/utility"
)

func correctSue(sue map[string]int, req map[string]int) bool {
	for k, v := range sue {
		if v != req[k] {
			return false
		}
	}
	return true
}

func correctSueRetroencabulator(sue map[string]int, req map[string]int) bool {
	for k, v := range sue {
		if k == "cats" || k == "trees" {
			if v <= req[k] {
				return false
			}
		} else if k == "pomeranians" || k == "goldfish" {
			if v >= req[k] {
				return false
			}
		} else if v != req[k] {
			return false
		}
	}
	return true
}

func mainPart2(sueList []map[string]int) {
	sueRequirements := utility.ParseLines("../sue_requirements.txt")

	reqMap := make(map[string]int)
	for _, req := range sueRequirements {
		split := strings.Split(req, ":")
		val, _ := strconv.Atoi(strings.TrimSpace(split[1]))
		reqMap[strings.TrimSpace(split[0])] = val
	}

	for idx, sue := range sueList {
		if correctSueRetroencabulator(sue, reqMap) {
			fmt.Printf("Sue %d got me the gift.\n", idx+1)
			break
		}
	}
}

func mainPart1(sueList []map[string]int) {
	sueRequirements := utility.ParseLines("../sue_requirements.txt")

	reqMap := make(map[string]int)
	for _, req := range sueRequirements {
		split := strings.Split(req, ":")
		val, _ := strconv.Atoi(strings.TrimSpace(split[1]))
		reqMap[strings.TrimSpace(split[0])] = val
	}

	for idx, sue := range sueList {
		if correctSue(sue, reqMap) {
			fmt.Printf("Sue %d got me the gift.\n", idx+1)
			break
		}
	}
}

func main() {
	sueLines := utility.ParseLines("../inputs.txt")

	sueList := make([]map[string]int, 0)

	for _, sue := range sueLines {
		noCommas := strings.ReplaceAll(sue, ",", "")
		split := strings.Split(noCommas, " ")
		sueMap := make(map[string]int)
		for i := 2; i < len(split); i = i + 2 {
			split2 := strings.Split(split[i], ":")
			val, _ := strconv.Atoi(strings.TrimSpace(split[i+1]))
			sueMap[strings.TrimSpace(split2[0])] = val
		}
		sueList = append(sueList, sueMap)
	}

	mainPart1(sueList)
	mainPart2(sueList)
}
