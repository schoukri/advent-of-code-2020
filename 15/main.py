#!/usr/bin/env python3

from collections import defaultdict

def speak(nums, stop):
    num_to_turns = defaultdict(list)
    for (turn, num) in enumerate(nums):
        num_to_turns[num].append(turn+1)
    last_num_spoken = nums[-1]
    for turn in range(len(num_to_turns)+1, stop+1):
        speak = 0
        if len(num_to_turns[last_num_spoken]) > 1:
            speak = num_to_turns[last_num_spoken][-1] - num_to_turns[last_num_spoken][-2]
        num_to_turns[speak].append(turn)
        last_num_spoken = speak
    return last_num_spoken

if __name__ == '__main__':
    assert(speak(nums=[0,3,6], stop=2020) == 436)
    print("PART 1:", speak(nums=[14,8,16,0,1,17], stop=2020))

    #assert(speak(nums=[0,3,6], stop=30000000) == 175594)
    print("PART 2:", speak(nums=[14,8,16,0,1,17], stop=30000000))
