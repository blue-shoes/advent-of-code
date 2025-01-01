package main

import (
	"crypto/md5"
	"encoding/hex"
	"fmt"
	"strconv"
	"strings"

	"github.com/blue-shoes/advent-of-code/utility"
)

func mainPart1(secret string) int {
	current := 1
	for {
		test := secret + strconv.Itoa(current)
		hash := md5.Sum([]byte(test))
		testMd5 := hex.EncodeToString(hash[:])
		if strings.HasPrefix(testMd5, "00000") {
			break
		}
		current += 1
	}
	fmt.Printf("The lowest number for the secret is %d.\n", current)

	return current
}

func mainPart2(secret string, startVal int) {
	current := startVal
	for {
		test := secret + strconv.Itoa(current)
		hash := md5.Sum([]byte(test))
		testMd5 := hex.EncodeToString(hash[:])
		if strings.HasPrefix(testMd5, "000000") {
			break
		}
		current += 1
	}
	fmt.Printf("The lowest number for the secret is %d.\n", current)
}

func main() {
	secret := utility.ParseLines("../inputs.txt")[0]

	val := mainPart1(secret)
	mainPart2(secret, val)
}
