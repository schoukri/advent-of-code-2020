<?php

$nums = [];

while (($line = fgets(STDIN)) !== false) {
    if ($line !== false) {
        if ($line === "\n") {
            continue;
        }
        $num = rtrim($line);
        $nums[] = $num;
    }
}

for ($i = 0; $i < count($nums); $i++) {
    for ($j = $i+1; $j < count($nums); $j++) {
        if ($nums[$i] + $nums[$j] == 2020 ) {
            printf("PART 1: %d\n", $nums[$i] * $nums[$j]);
        }
        for ($k = $j+1; $k < count($nums); $k++) {
            if ($nums[$i] + $nums[$j] + $nums[$k] == 2020) {
                printf("PART 2: %d\n", $nums[$i] * $nums[$j] * $nums[$k]);
            }
        }
    }
}
