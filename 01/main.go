package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"os"
	"strconv"
)

func main() {

	filePath := flag.String("file", "", "file containing the input data")
	doPart2 := flag.Bool("part2", false, "do part 2")
	flag.Parse()

	if *filePath == "" {
		log.Fatal("file not specified")
	}

	file, err := os.Open(*filePath)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	nums := make([]int, 0)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		value, err := strconv.Atoi(line)
		if err != nil {
			log.Fatalf("cannot parse line '%s' as int: %v", line, err)
		}

		if value <= 2020 {
			nums = append(nums, value)
		}
	}

	if *doPart2 {
		for i, a := range nums {
			for j, b := range nums {
				if i == j {
					continue
				}
				if a+b >= 2020 {
					continue
				}
				for h, c := range nums {
					if j == h || i == h {
						continue
					}
					if a+b+c == 2020 {
						fmt.Printf("PART 2: a=%v, b=%v, c=%v, total=%v\n", a, b, c, a*b*c)
						os.Exit(0)
					}
				}
			}
		}
	} else {
		for i, a := range nums {
			for j, b := range nums {
				if i == j {
					continue
				}
				if a+b == 2020 {
					fmt.Printf("PART 1: a=%v, b=%v, total=%v\n", a, b, a*b)
					os.Exit(0)
				}

			}
		}
	}
}
