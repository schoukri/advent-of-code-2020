#!/usr/bin/env perl

use strict;
use warnings;
$/ = ""; # paragraph mode

my ($part1, $part2) = (0, 0);
while (my $group = <>) {
    chomp $group;
    my @people = split /\n/, $group;
    my %questions;
    for my $q (split '', $group) {
        next unless $q =~ /\w/;
        $part2++ if ++$questions{$q} == scalar(@people);
    }
    $part1 += scalar(keys %questions);
}
print "PART1: $part1\n";
print "PART2: $part2\n";
