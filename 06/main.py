import sys
import re
from collections import Counter

(part1, part2) = (0, 0)
for group in re.split("\n\n", sys.stdin.read().rstrip()):
    people = re.split("\n", group)
    questions = Counter()
    for q in group:
        if not re.match("\w", q): continue
        questions[q] += 1
        if questions[q] == len(people): part2 += 1
    part1 += len(questions)

print("PART 1:", part1)
print("PART 2:", part2)
