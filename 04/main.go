package main

import (
	"bufio"
	"errors"
	"flag"
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"
	"strings"
)

func main() {

	filePath := flag.String("file", "input.txt", "file containing the input data")
	doPart2 := flag.Bool("part2", false, "do part 2")
	flag.Parse()

	lines, err := readFile(*filePath)
	if err != nil {
		log.Fatalf("cannot read file %s: %v", *filePath, err)
	}

	// cid (Country ID) - ignored, missing or not.
	required := map[string]func(val string) bool{
		// byr (Birth Year) - four digits; at least 1920 and at most 2002.
		"byr": func(val string) bool {
			num := mustParseInt(val)
			return num >= 1920 && num <= 2002
		},
		// iyr (Issue Year) - four digits; at least 2010 and at most 2020.
		"iyr": func(val string) bool {
			num := mustParseInt(val)
			return num >= 2010 && num <= 2020
		},
		// eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
		"eyr": func(val string) bool {
			num := mustParseInt(val)
			return num >= 2020 && num <= 2030
		},
		// hgt (Height) - a number followed by either cm or in:
		// If cm, the number must be at least 150 and at most 193.
		// If in, the number must be at least 59 and at most 76.
		"hgt": func(val string) bool {
			re := regexp.MustCompile(`^(\d+)(cm|in)$`)
			matches := re.FindStringSubmatch(val)
			if matches == nil {
				return false
			}
			num := mustParseInt(matches[1])
			unit := mustParseString(matches[2])
			return (unit == "cm" && num >= 150 && num <= 193) || (unit == "in" && num >= 59 && num <= 76)
		},
		// hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
		"hcl": func(val string) bool {
			re := regexp.MustCompile(`^#[0-9a-f]{6}$`)
			return re.MatchString(val)
		},
		// ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
		"ecl": func(val string) bool {
			re := regexp.MustCompile(`^(amb|blu|brn|gry|grn|hzl|oth)$`)
			return re.MatchString(val)
		},
		// pid (Passport ID) - a nine-digit number, including leading zeroes.
		"pid": func(val string) bool {
			re := regexp.MustCompile(`^\d{9}$`)
			return re.MatchString(val)
		},
	}
	answer := 0
	passport := make(map[string]string)
	for _, line := range lines {

		// empty line: check the passport fields
		if line == "" {
			valid := true
			for field, isValidFn := range required {
				if val, ok := passport[field]; !ok || (*doPart2 && !isValidFn(val)) {
					valid = false
					break
				}
			}
			if valid {
				answer++
			}
			passport = make(map[string]string)
			continue
		}
		terms := strings.Fields(line)
		for _, term := range terms {
			pair := strings.SplitN(term, ":", 2)
			passport[pair[0]] = pair[1]
		}

	}
	if *doPart2 {
		fmt.Printf("PART 2: %d\n", answer)
	} else {
		fmt.Printf("PART 1: %d\n", answer)
	}
}

func readFile(path string) ([]string, error) {
	if path == "" {
		return nil, errors.New("file path not specified")
	}

	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	lines := make([]string, 0)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		return nil, err
	}

	return lines, nil
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
