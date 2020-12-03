package main

import (
	"bufio"
	"errors"
	"flag"
	"fmt"
	"log"
	"os"
)

type Grid struct {
	data       [][]bool
	x, y       int
	maxX, maxY int
}

type Offset struct {
	x, y int
}

func main() {

	filePath := flag.String("file", "input.txt", "file containing the input data")
	flag.Parse()

	lines, err := readFile(*filePath)
	if err != nil {
		log.Fatalf("cannot read file %s: %v", *filePath, err)
	}

	part1 := 0
	grid := NewGrid(lines)
	for grid.Move(Offset{3, 1}) {
		if grid.AtTree() {
			part1++
		}
	}
	fmt.Printf("PART 1: %d\n", part1)

	offsets := []Offset{
		{1, 1},
		{3, 1},
		{5, 1},
		{7, 1},
		{1, 2},
	}

	part2 := 1
	for _, offset := range offsets {
		count := 0
		grid.Reset()
		for grid.Move(offset) {
			if grid.AtTree() {
				count++
			}
		}
		part2 *= count
	}
	fmt.Printf("PART 2: %d\n", part2)
}

// reset grid to starting point
func (g *Grid) Reset() {
	g.x = 0
	g.y = 0
}

func (g *Grid) Move(o Offset) bool {
	// if we are on the last row and can't move down, return false
	if g.y+o.y > g.maxY {
		return false
	}
	g.y += o.y
	g.x += o.x
	if g.x > g.maxX {
		g.x -= (g.maxX + 1)
	}
	return true
}

func (g *Grid) AtTree() bool {
	return g.data[g.y][g.x]
}

func NewGrid(lines []string) *Grid {

	grid := &Grid{
		maxY: len(lines) - 1,
	}

	grid.data = make([][]bool, len(lines))
	for y, line := range lines {
		row := make([]bool, len(line))
		for x, char := range line {
			if char == '#' {
				row[x] = true
			}
		}
		grid.data[y] = row
		maxX := len(line) - 1
		if maxX > grid.maxX {
			grid.maxX = maxX
		}
	}
	return grid
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
