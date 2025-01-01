package main

import (
	"fmt"
	"regexp"

	"github.com/blue-shoes/advent-of-code/utility"
	"github.com/glenn-brown/golang-pkg-pcre/src/pkg/pcre"
)

func isNice(line string) bool {
	r1, _ := regexp.Compile(`ab|cd|pq|xy`)
	r2, _ := regexp.Compile(`[aeiou]\w*[aeiou]\w*[aeiou]`)
	r3 := pcre.MustCompile(`([a-z])\1`, 0)

	if r1.MatchString(line) {
		return false
	}
	if !r2.MatchString(line) {
		return false
	}

	return r3.MatcherString(line, 0).Matches()
}

func isNicer(line string) bool {
	test1 := false
	test2 := false
	for idx, r := range line[:len(line)-2] {
		twoRune := line[idx : idx+2]
		if r == rune(line[idx+2]) {
			test1 = true
		}
		if !test2 {
			for idx2 := idx + 2; idx2 < len(line)-1; idx2++ {
				if line[idx2:idx2+2] == twoRune {
					test2 = true
				}
			}
		}
		if test1 && test2 {
			return true
		}
	}
	return false
}

func mainPart1(lines []string) {
	niceCount := 0
	for _, line := range lines {
		if isNice(line) {
			niceCount += 1
		}
	}
	fmt.Printf("There are %d nice strings.\n", niceCount)
}

func mainPart2(lines []string) {
	niceCount := 0
	for _, line := range lines {
		if isNicer(line) {
			niceCount += 1
		}
	}
	fmt.Printf("There are %d nicer strings.\n", niceCount)
}

func main() {
	lines := utility.ParseLines("../inputs.txt")

	mainPart1(lines)
	mainPart2(lines)
}
