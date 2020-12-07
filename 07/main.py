import sys
import re
from collections import Counter

# bright white bags contain 1 shiny gold bag.
# muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
# faded blue bags contain no other bags.
def main():

    rules = {}
    for rule in re.split("\n", sys.stdin.read().rstrip()):
        bags = {}
        for bag_count in re.findall(" (\d+) (\w+ \w+) bags?[.,]", rule):
            bags[bag_count[1]] = int(bag_count[0])
        bag = re.match("(\w+ \w+) bags contain", rule)
        rules[bag.group(1)] = bags

    # find the total num of distinct bags that can contain 1 shiny gold bag
    found1 = {}
    find_part_1(rules, 'shiny gold', found1)
    print("PART 1:", len(found1))

    # find the total number of nested bags that are contained within 1 shiny gold bag
    found2 = []
    find_part_2(rules, 'shiny gold', 1, found2)
    part2 = 0
    for item in found2:
        part2 += item[1] * item[2]
    print("PART 2:", part2)

def find_part_1(rules, target, found):
    for bag, contents in rules.items():
        for bag_inside in contents.keys():
            if bag_inside == target:
                if bag not in found: found[bag]=True
                find_part_1(rules, bag, found)

def find_part_2(rules, target, count, found):
    contents = rules[target]
    for bag_inside, bag_count in contents.items():
        found.append([bag_inside, count, bag_count])
        find_part_2(rules, bag_inside, count * bag_count, found)

if __name__ == '__main__':
    main()
