#!/usr/bin/env perl

use strict;
use warnings;

my @nums = <>;

for (my $i = 0; $i < scalar(@nums); $i++) {
  for (my $j = $i+1; $j < scalar(@nums); $j++) {
    if ($nums[$i] + $nums[$j] == 2020 ) {
      printf "PART 1: %d\n", $nums[$i] * $nums[$j]
    }
    for (my $k = $j+1; $k < scalar(@nums); $k++) {
      if ($nums[$i] + $nums[$j] + $nums[$k] == 2020) {
        printf "PART 2: %d\n", $nums[$i] * $nums[$j] * $nums[$k]
      }
    }
  }
}
