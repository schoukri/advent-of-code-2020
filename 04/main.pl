#!/usr/bin/env perl

use strict;
use warnings;
$/ = ""; # paragraph mode

my($part1, $part2) = (0, 0);
my @required = qw(byr iyr eyr hgt hcl ecl pid);
while (<>) {
    my %passport = map {split ':'} split(/\s+/);
    is_valid_part1(\%passport) && $part1++;
    is_valid_part2(\%passport) && $part2++;
}

print "PART 1: $part1\n";
print "PART 2: $part2\n";

sub is_valid_part1 {
    my($passport) = shift;
    return scalar(@required) == grep {exists $passport->{$_}} @required;
}

sub is_valid_part2 {
    my($passport) = shift;
    return is_valid_part1($passport) &&
        ($passport->{byr} =~ /^(\d{4})$/ && $1 >= 1920 && $1 <= 2002) &&
        ($passport->{iyr} =~ /^(\d{4})$/ && $1 >= 2010 && $1 <= 2020) &&
        ($passport->{eyr} =~ /^(\d{4})$/ && $1 >= 2020 && $1 <= 2030) &&
        ($passport->{hgt} =~ /^(\d+)(cm|in)$/ && (($1 >= 150 && $1 <= 193 && $2 eq 'cm') || ($1 >= 59 && $1 <= 76 && $2 eq 'in'))) &&
        ($passport->{hcl} =~ /^#[0-9a-f]{6}$/) &&
        ($passport->{ecl} =~ /^(amb|blu|brn|gry|grn|hzl|oth)$/) &&
        ($passport->{pid} =~ /^\d{9}$/);
}
