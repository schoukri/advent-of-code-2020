#!/usr/bin/env perl

use strict;
use warnings;
$/ = ""; # paragraph mode

my($part1, $part2) = (0, 0);
while (<>) {
    $part1++ if 7 == scalar(() = $_ =~ /\b(byr|iyr|eyr|hgt|hcl|ecl|pid):/g);
    $part2++ if
        /\bbyr:(19[2-9]\d|200[012])\b/ &&
        /\biyr:20(1\d|20)\b/ &&
        /\beyr:20(2\d|30)\b/ &&
        /\bhgt:((1([5-8]\d|9[0-3])cm)|((59|6\d|7[0-6])in))\b/ &&
        /\bhcl:#[0-9a-f]{6}\b/ &&
        /\becl:(amb|blu|brn|gry|grn|hzl|oth)\b/ &&
        /\bpid:\d{9}\b/;
}

print "PART 1: $part1\n";
print "PART 2: $part2\n";
