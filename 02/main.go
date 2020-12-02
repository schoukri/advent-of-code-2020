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

var passwordRegexp = regexp.MustCompile(`^(\d+)-(\d+) (\w): (\w+)$`)

type PasswordPolicy struct {
	Min      int
	Max      int
	Letter   string
	Password string
}

func main() {

	filePath := flag.String("file", "input.txt", "file containing the input data")
	flag.Parse()

	lines, err := readFile(*filePath)
	if err != nil {
		log.Fatalf("cannot read file %s: %v", *filePath, err)
	}

	answer1 := 0
	answer2 := 0
	for _, line := range lines {

		pp := mustParseLine(line)

		count1 := strings.Count(pp.Password, pp.Letter)
		if count1 >= pp.Min && count1 <= pp.Max {
			answer1++
		}

		count2 := 0
		if string(pp.Password[pp.Min-1]) == pp.Letter {
			count2++
		}
		if string(pp.Password[pp.Max-1]) == pp.Letter {
			count2++
		}
		if count2 == 1 {
			answer2++
		}
	}
	fmt.Printf("PART 1: %d\n", answer1)
	fmt.Printf("PART 2: %d\n", answer2)
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

func mustParseLine(line string) PasswordPolicy {

	matches := passwordRegexp.FindStringSubmatch(line)
	if matches == nil {
		log.Fatalf("cannot parse line: %s", line)
	}

	return PasswordPolicy{
		Min:      mustParseInt(matches[1]),
		Max:      mustParseInt(matches[2]),
		Letter:   mustParseString(matches[3]),
		Password: mustParseString(matches[4]),
	}
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
