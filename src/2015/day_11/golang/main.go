package main

import (
	"fmt"
	"slices"

	"github.com/blue-shoes/advent-of-code/utility"
)

func passesRule1(password []int) bool {
	for i := 0; i < len(password)-2; i++ {
		if password[i]+1 == password[i+1] && password[i]+2 == password[i+2] {
			return true
		}
	}
	return false
}

var illegalRunes = [3]int{int('i' - 'a'), int('l' - 'a'), int('o' - 'a')}

func passesRule2(password []int) bool {
	for _, illegal := range illegalRunes {
		if slices.Contains(password, illegal) {
			return false
		}
	}
	return true
}

func passesRule3(password []int) bool {
	foundOne := false
	for i := 0; i < len(password)-1; i++ {
		if password[i] == password[i+1] {
			if foundOne {
				return true
			}
			foundOne = true
			i++
		}
	}
	return false

}

func passes(pw []int) bool {
	return passesRule1(pw) && passesRule2(pw) && passesRule3(pw)
}

func recursiveIncrement(password []int, idx int) []int {
	updateVal := (password[idx] + 1) % 26
	if updateVal == 0 {
		password = recursiveIncrement(password, idx-1)
	}
	password[idx] = updateVal
	return password
}

func incrementPassword(password []int) []int {
	return recursiveIncrement(password, len(password)-1)
}

func mainPart1(password string) string {

	intPassword := make([]int, len(password))
	for i := 0; i < len(password); i++ {
		intPassword[i] = int(rune(password[i]) - 'a')
	}
	for {
		intPassword = incrementPassword(intPassword)
		if passes(intPassword) {
			break
		}
	}
	newPassword := ""
	for i := 0; i < len(password); i++ {
		newPassword += string(rune(intPassword[i] + 'a'))
	}
	fmt.Printf("The next new password is %s.\n", newPassword)
	return newPassword
}

func main() {
	password := utility.ParseLines("../inputs.txt")[0]

	newPassword := mainPart1(password)
	mainPart1(newPassword)
}
