package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"
)

var bagRegexp = regexp.MustCompile(`^(\w+ \w+) bags contain`)
var contentsRegexp = regexp.MustCompile(` (\d+) (\w+ \w+) bags?[.,]`)

type Counter map[string]int
type Rules map[string]Counter

func main() {

	filePath := flag.String("file", "input.txt", "file containing the input data")
	flag.Parse()

	lines := mustReadFile(*filePath)
	rules := parseLines(lines)

	found1 := findOuterBags(rules, "shiny gold", make(Counter))
	fmt.Println("PART 1:", len(found1))

	found2 := findNestedBags(rules, "shiny gold", 1, make(Counter))
	answer2 := 0
	for _, count := range found2 {
		answer2 += count
	}
	fmt.Println("PART 2:", answer2)
}

func findOuterBags(rules Rules, target string, found Counter) Counter {
	for bag, contents := range rules {
		if _, ok := contents[target]; ok {
			found[bag] = 1
			found = findOuterBags(rules, bag, found)
		}
	}
	return found
}

func findNestedBags(rules Rules, target string, count int, found Counter) Counter {
	contents := rules[target]
	for bag, bagCount := range contents {
		found[bag] += (count * bagCount)
		found = findNestedBags(rules, bag, count*bagCount, found)
	}
	return found
}

func parseLines(lines []string) Rules {
	rules := make(Rules)
	for _, line := range lines {
		matches := bagRegexp.FindStringSubmatch(line)
		if matches == nil {
			log.Fatalf("cannot parse line: %s", line)
		}
		outerBag := mustParseString(matches[1])

		contentMatches := contentsRegexp.FindAllStringSubmatch(line, -1)
		for _, match := range contentMatches {
			quantity := mustParseInt(match[1])
			innerBag := mustParseString(match[2])
			if _, ok := rules[outerBag]; !ok {
				rules[outerBag] = make(Counter)
			}
			rules[outerBag][innerBag] = quantity
		}
	}
	return rules
}

func mustReadFile(path string) []string {
	if path == "" {
		log.Fatalf("file path not specified: %v", path)
	}

	file, err := os.Open(path)
	if err != nil {
		log.Fatalf("cannot open file: %v", err)
	}
	defer file.Close()

	lines := make([]string, 0)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		log.Fatalf("scanner error: %v", err)
	}

	return lines
}

func mustParseInt(s string) int {
	i, err := strconv.Atoi(s)
	if err != nil {
		log.Fatalf("cannot convert string %s to integer: %v", s, err)
	}
	return i
}
func mustParseString(s string) string {
	if s == "" {
		log.Fatalf("string cannot be empty")
	}
	return s
}
