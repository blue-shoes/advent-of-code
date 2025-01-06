package main

import (
	"encoding/json"
	"fmt"
	"log"
	"regexp"

	"github.com/blue-shoes/advent-of-code/utility"
)

func mainPart1(line string) int {
	r1 := regexp.MustCompile(`(-?\d+)`)
	matches := r1.FindAllString(line, -1)

	sum := utility.Sum(utility.StringArrayToInts(matches))
	fmt.Printf("The document sum is %d.\n", sum)
	return sum
}

func parseTopLevelMaps(message []*json.RawMessage) []map[string]interface{} {
	maps := make([]map[string]interface{}, 0)
	for i := 0; i < len(message); i++ {
		var objmap map[string]interface{}
		if err := json.Unmarshal(*message[i], &objmap); err != nil {
			var submessage []*json.RawMessage
			json.Unmarshal(*message[i], &submessage)
			maps = append(maps, parseTopLevelMaps(submessage)...)
			continue
		}
		maps = append(maps, objmap)
	}

	return maps
}

func getRedSumArray(a []interface{}, parentRed bool) int {
	subMaps := make([]map[string]interface{}, 0)
	subArrays := make([][]interface{}, 0)
	levelSum := 0
	red := parentRed
	for _, value := range a {
		switch v := value.(type) {
		case string:
			//nothing
		case int:
			levelSum += value.(int)
		case float64:
			levelSum += int(value.(float64))
		case []interface{}:
			subArrays = append(subArrays, value.([]interface{}))
		case map[string]interface{}:
			subMaps = append(subMaps, value.(map[string]interface{}))
		default:
			panic(v)
		}
	}

	sublevelSum := 0
	for _, m2 := range subMaps {
		sublevelSum += getRedSum(m2, red)
	}
	for _, a := range subArrays {
		sublevelSum += getRedSumArray(a, red)
	}

	if red {
		return levelSum + sublevelSum
	}
	return sublevelSum
}

func getRedSum(m map[string]interface{}, parentRed bool) int {
	subMaps := make([]map[string]interface{}, 0)
	subArrays := make([][]interface{}, 0)
	levelSum := 0
	red := parentRed
	for _, value := range m {
		switch v := value.(type) {
		case string:
			if value == "red" {
				red = true
			}
		case int:
			levelSum += value.(int)
		case float64:
			levelSum += int(value.(float64))
		case []interface{}:
			subArrays = append(subArrays, value.([]interface{}))
		case map[string]interface{}:
			subMaps = append(subMaps, value.(map[string]interface{}))
		default:
			panic(v)
		}
	}

	sublevelSum := 0
	for _, m2 := range subMaps {
		sublevelSum += getRedSum(m2, red)
	}
	for _, a := range subArrays {
		sublevelSum += getRedSumArray(a, red)
	}

	if red {
		return levelSum + sublevelSum
	}
	return sublevelSum
}

func mainPart2_json(line string, val int) {

	var objmap []*json.RawMessage
	if err := json.Unmarshal([]byte(line), &objmap); err != nil {
		log.Fatal(err)
		return
	}

	topLevelMaps := parseTopLevelMaps(objmap)

	sum := 0
	for _, m := range topLevelMaps {
		sum += getRedSum(m, false)
	}

	fmt.Printf("Total non-red sum is %d.\n", val-sum)
}

func main() {
	line := utility.ParseLines("../inputs.txt")[0]
	v := mainPart1(line)
	mainPart2_json(line, v)
}
