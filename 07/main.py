import sys, re

def main():

    rules = dict()
    for rule in re.split("\n", sys.stdin.read().rstrip()):
        bags = dict()
        for bag_count in re.findall(" (\d+) (\w+ \w+) bags?[.,]", rule):
            bags[bag_count[1]] = int(bag_count[0])
        bag = re.match("(\w+ \w+) bags contain", rule)
        rules[bag.group(1)] = bags

    # find the total num of outer bags that can contain 1 shiny gold bag
    found1 = find_outer_bags(rules, 'shiny gold')
    print("PART 1:", len(found1))

    # find the total number of nested bags that are contained within 1 shiny gold bag
    found2 = find_nested_bags(rules, 'shiny gold')
    print("PART 2:", sum(map(lambda x: x[1] * x[2], found2)))

def find_outer_bags(rules, target, found=set()):
    for bag, contents in rules.items():
        if target in contents:
            found.add(bag)
            found = find_outer_bags(rules, bag, found)
    return found

def find_nested_bags(rules, target, count=1, found=list()):
    contents = rules[target]
    for bag_inside, bag_count in contents.items():
        found.append([bag_inside, count, bag_count])
        found = find_nested_bags(rules, bag_inside, count * bag_count, found)
    return found

if __name__ == '__main__':
    main()
