package main

import (
	"fmt"
	"regexp"
	"slices"
	"strconv"

	"github.com/blue-shoes/advent-of-code/utility"
)

type base int

const (
	ASSIGN base = iota
	AND
	OR
	NOT
	RSHIFT
	LSHIFT
)

type Gate struct {
	operator               base
	input1, input2, output string
}

func createGate(match []string, operator base) Gate {
	if _, err := strconv.Atoi(match[1]); err == nil {
		return Gate{operator: operator, input1: match[3], input2: match[1], output: match[4]}
	}
	return Gate{operator: operator, input1: match[1], input2: match[3], output: match[4]}
}

func mainPart2(initValues map[string]int, gates []Gate, aVal int) {
	values := make(map[string]int)
	for k, v := range initValues {
		values[k] = v
	}
	values["b"] = aVal

	mainPart1(values, gates)
}

func mainPart1(initValues map[string]int, gates []Gate) int {
	values := make(map[string]int)
	for k, v := range initValues {
		values[k] = v
	}
	operGates := make([]Gate, len(gates))
	copy(operGates, gates)
	for {
		toRemove := make([]Gate, 0)
		for _, gate := range operGates {
			if inp1, present := values[gate.input1]; present {
				if gate.operator == NOT {
					values[gate.output] = int(^uint16(inp1))
				} else if gate.operator == ASSIGN {
					values[gate.output] = inp1
				} else if gate.operator == LSHIFT {
					shift, _ := strconv.Atoi(gate.input2)
					values[gate.output] = inp1 << shift
				} else if gate.operator == RSHIFT {
					shift, _ := strconv.Atoi(gate.input2)
					values[gate.output] = inp1 >> shift
				} else if inp2, present := values[gate.input2]; present {
					if gate.operator == AND {
						values[gate.output] = inp1 & inp2
					} else if gate.operator == OR {
						values[gate.output] = inp1 | inp2
					}
				} else if inp2, err := strconv.Atoi(gate.input2); err == nil {
					if gate.operator == AND {
						values[gate.output] = inp1 & inp2
					} else if gate.operator == OR {
						values[gate.output] = inp1 | inp2
					}
				}
			}
			if _, present := values[gate.output]; present {
				toRemove = append(toRemove, gate)
			}
		}

		operGates = slices.DeleteFunc(operGates, func(g Gate) bool { return slices.Contains(toRemove, g) })
		if len(operGates) == 0 {
			break
		}
		if _, present := values["a"]; present {
			break
		}
	}

	fmt.Printf("Wire a has value %d\n", values["a"])
	return values["a"]
}

func main() {
	lines := utility.ParseLines("../inputs.txt")
	assign := regexp.MustCompile(`^(\d+) -> (\w+)`)
	assign2 := regexp.MustCompile(`^(\w+) -> (\w+)`)
	andOr := regexp.MustCompile(`(\S+) (AND|OR) (\S+) -> (\w+)`)
	shift := regexp.MustCompile(`(\S+) (R|L)SHIFT (\S+) -> (\w+)`)
	not := regexp.MustCompile(`NOT (\S+) -> (\w+)`)

	initValues := map[string]int{}
	gates := make([]Gate, 0)

	for _, line := range lines {
		if match := assign.FindAllStringSubmatch(line, -1); len(match) > 0 {
			val, _ := strconv.Atoi(match[0][1])
			initValues[match[0][2]] = val
		} else if match := assign2.FindAllStringSubmatch(line, -1); len(match) > 0 {
			gates = append(gates, Gate{operator: ASSIGN, input1: match[0][1], output: match[0][2]})
		} else if match := andOr.FindAllStringSubmatch(line, -1); len(match) > 0 {
			if match[0][2] == "OR" {
				gates = append(gates, createGate(match[0], OR))
			} else {
				gates = append(gates, createGate(match[0], AND))
			}
		} else if match := shift.FindAllStringSubmatch(line, -1); len(match) > 0 {
			if match[0][2] == "L" {
				gates = append(gates, createGate(match[0], LSHIFT))
			} else {
				gates = append(gates, createGate(match[0], RSHIFT))
			}
		} else {
			match := not.FindAllStringSubmatch(line, -1)
			gates = append(gates, Gate{operator: NOT, input1: match[0][1], output: match[0][2]})
		}
	}
	fmt.Println(initValues)
	aVal := mainPart1(initValues, gates)
	mainPart2(initValues, gates, aVal)
}
