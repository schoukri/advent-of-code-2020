#!/usr/bin/env python3

import sys, re, collections

class Decoder:

    def __init__(self, lines: list):
        rules_re = re.compile(r'^([\w\s]+): (\d+)-(\d+) or (\d+)-(\d+)$')
        rules = dict()
        in_your = False
        in_nearby = False
        tickets = []
        for line in lines:
            if rules_match := rules_re.match(line):
                rules[rules_match.group(1)] = [
                    (int(rules_match.group(2)), int(rules_match.group(3))),
                    (int(rules_match.group(4)), int(rules_match.group(5))),
                ]
            elif re.search(r'^your ticket:$', line) is not None:
                in_your = True
            elif re.search(r'^nearby tickets:$', line) is not None:
                in_nearby = True
            elif in_your or in_nearby:
                tickets.append([int(num) for num in line.split(',')])
                if in_your:
                    in_your = False
        self.rules = rules
        self.your_ticket = tickets[0]
        self.nearby_tickets = tickets[1:]

    def valid_tickets(self) -> list:
        """return the list of tickets that do not contain any invalid values"""
        invalid_tickets = self.invalid_ticket_values_counter().keys()
        return [t for (i, t) in enumerate(self.nearby_tickets) if i not in invalid_tickets]


    def is_valid_ticket_value(self, value: int) -> bool:
        """return True if the specified ticket value is valid with at least one rule"""
        for rule in self.rules.values():
            for (low, high) in rule:
                if low <= value <= high:
                    return True
        return False

    def invalid_ticket_values_counter(self) -> collections.Counter:
        """return a Counter object of invalid tickets (key is ticket index and value is sum of invalid ticket values)"""
        counter = collections.Counter()
        for i, ticket in enumerate(self.nearby_tickets):
            for value in ticket:
                if not self.is_valid_ticket_value(value):
                    counter[i] += value
        return counter


    def decode_field_names(self) -> list:
        """return list of decoded field names in their correct order"""

        # prepare 2D list of all field names that are valid in each field position
        valid_tickets = self.valid_tickets()
        valid_field_names = []
        for field_num in range(len(valid_tickets[0])):
            field_values = [ticket[field_num] for ticket in valid_tickets]
            valid_fields = []
            for (name, rule) in self.rules.items():
                is_valid = True
                for value in field_values:
                    valid_found = list(filter(lambda x: x[0] <= value <= x[1], rule))
                    if len(valid_found) == 0:
                        is_valid = False
                        break
                if is_valid:
                    valid_fields.append(name)
            valid_field_names.append(valid_fields)

        # decode the 2D list so that only 1 valid field remains in each field position
        while True:
            modified = False
            only_one = [fields[0] for fields in valid_field_names if len(fields) == 1]
            for field_name in only_one:
                for fields in valid_field_names:
                    if len(fields) > 1 and field_name in fields:
                        fields.remove(field_name)
                        modified = True
            if not modified:
                break

        # now that the decoded 2D list only has 1 item in each of the nested lists,
        # convert the 2D list into a 1D list and return it
        return [fields[0] for fields in valid_field_names]


if __name__ == '__main__':
    lines = open('input.txt').readlines()
    decoder = Decoder(lines)

    invalid_tickets = decoder.invalid_ticket_values_counter()
    print("PART 1:", sum(invalid_tickets.values()))

    field_names = decoder.decode_field_names()
    part2 = 1
    for i, value in enumerate(decoder.your_ticket):
        if field_names[i].startswith('departure'):
            part2 *= value
    print("PART 2:", part2)
