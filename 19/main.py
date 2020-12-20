#!/usr/bin/env python3

#import graphlib
import re
from collections import defaultdict
from typing import List

class Rules():
    letter_re = re.compile(r'^(\d+): \"([ab])\"$')
    nums_re = re.compile(r'^(\d+): (\d+( \d+)*)$')
    nums_alt_re = re.compile(r'^(\d+): (\d+( \d+)* \| (\d+ )*\d+)$')
    message_re = re.compile(r'^([ab]+)$')
    cycle_one_re = re.compile(r'^(\d+): (\d+) \| \2 \1$')
    cycle_two_re = re.compile(r'^(\d+): (\d+) (\d+) \| \2 \1 \3$')
    digit_re = re.compile(r'\d')

    def __init__(self, lines: List[str]):
        rules = defaultdict()
        messages_start = 0
        for (i, line) in enumerate(lines):
            if match := Rules.letter_re.match(line):
                rules[match.group(1)] = match.group(2)
            elif match := Rules.cycle_one_re.match(line):
                # 1 or more of the rule
                rules[match.group(1)] = f'({match.group(2)})+'
            elif match := Rules.cycle_two_re.match(line):
                (x, y) = (match.group(2), match.group(3))
                rule = ''
                # optional multiple nested pairs
                # technically there can be an infinite number, but we will stop at 10
                for i in range(10):
                    rule = f'({x} {rule} {y})?'
                # required final outer pair
                rules[match.group(1)] = f'({x} {rule} {y})'
            elif match := Rules.nums_re.match(line):
                rules[match.group(1)] = match.group(2)
            elif match := Rules.nums_alt_re.match(line):
                rules[match.group(1)] = '(' + match.group(2) + ')'
            elif match := Rules.message_re.match(line):
                messages_start = i
                break
        self.rules = rules
        self.messages = lines[messages_start:]

    # def update(rule: str, value: str):
    #     self.rules[rule] = value

    def run(self):
        while True:
            changes = 0
            # look for rules that are ready (the ones that do not have any num references to other rules)
            ready_nums = [k for (k,v) in self.rules.items() if not Rules.digit_re.search(v)]
            # search for the num references of the ready rules in all other rules
            # and replace their num reference with the actual rule value
            for target in ready_nums:
                for key in self.rules.keys():
                    new_value = re.sub(r'\b' + target + r'\b', self.rules[target], self.rules[key])
                    if self.rules[key] != new_value:
                        self.rules[key] = new_value
                        changes += 1
            # once no rules are updated, we are done
            if changes == 0:
                break

        # strip all the whitespace
        for key in self.rules.keys():
            self.rules[key] = re.sub(r'\s+', '', self.rules[key])

    def count_matching_messages(self, rule: int) -> int:
        # count the number of messages that match rule 0 (zero)
        rule_re = re.compile(r'^' + self.rules[str(rule)] + r'$')
        count = 0
        for message in self.messages:
            if match := rule_re.match(message):
                count += 1
        return count

if __name__ == '__main__':
    lines1 = [line.rstrip("\n") for line in open('input1.txt').readlines()]
    rules1 = Rules(lines1)
    rules1.run()
    print("PART 1:", rules1.count_matching_messages(rule=0))

    lines2 = [line.rstrip("\n") for line in open('input2.txt').readlines()]
    rules2 = Rules(lines2)
    rules2.run()
    print("PART 2:", rules2.count_matching_messages(rule=0))
