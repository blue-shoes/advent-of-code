package main

import (
	"fmt"
	"strings"

	"github.com/blue-shoes/advent-of-code/utility"
)

var regA, regB int

type Instr struct {
	command, register string
	offset            int
}

func getRegisterValue(reg string) int {
	if reg == "a" {
		return regA
	}
	return regB
}

func setVal(val int, reg string) {
	if reg == "a" {
		regA = val
	} else {
		regB = val
	}
}

func hlf(reg string) {
	currentVal := getRegisterValue(reg)
	setVal(currentVal/2, reg)
}

func tpl(reg string) {
	currentVal := getRegisterValue(reg)
	setVal(currentVal*3, reg)
}

func inc(reg string) {
	currentVal := getRegisterValue(reg)
	setVal(currentVal+1, reg)
}

func jmp(idx, offset int) int {
	return idx + offset - 1
}

func jie(idx, offset int, reg string) int {
	currentVal := getRegisterValue(reg)
	if currentVal%2 == 0 {
		return jmp(idx, offset)
	}
	return idx
}

func jio(idx, offset int, reg string) int {
	currentVal := getRegisterValue(reg)
	if currentVal == 1 {
		return jmp(idx, offset)
	}
	return idx
}

func mainPart(instructions []Instr) {
	for i := 0; i < len(instructions); i++ {
		inst := instructions[i]
		switch inst.command {
		case "hlf":
			hlf(inst.register)
		case "tpl":
			tpl(inst.register)
		case "inc":
			inc(inst.register)
		case "jmp":
			i = jmp(i, inst.offset)
		case "jie":
			i = jie(i, inst.offset, inst.register)
		case "jio":
			i = jio(i, inst.offset, inst.register)
		}
	}
	fmt.Printf("Register b is %d after the program completes\n", regB)
}

func main() {
	regA = 0
	regB = 0

	instructionLines := utility.ParseLines("../inputs.txt")
	instructions := []Instr{}
	for _, line := range instructionLines {
		line = strings.ReplaceAll(line, ",", "")
		split := strings.Split(line, " ")
		if len(split) == 3 {
			instructions = append(instructions, Instr{command: split[0], register: split[1], offset: utility.Atoi(split[2])})
		} else {
			if split[0] == "jmp" {
				instructions = append(instructions, Instr{command: split[0], offset: utility.Atoi(split[1])})
			} else {
				instructions = append(instructions, Instr{command: split[0], register: split[1]})
			}
		}
	}

	mainPart(instructions)

	regA = 1
	regB = 0

	mainPart(instructions)
}
