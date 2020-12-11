import sys, re
from collections import Counter

def part_1(nums):
    """Return the number of adjacent adaptors with a delta of 1 multiplied by those with a delta of 3"""
    counter = Counter()
    prev = 0
    for num in nums:
        counter[num - prev] += 1
        prev = num
    return counter[1] * counter[3]


def part_2(nums):
    """Return the total number of unique pathways that the adaptors can be arranged."""
    # Partition the adaptors into segments where the difference between consecutive
    # adaptors is equal to 3. The beginning and end adaptors of each segment will
    # always be present in every valid pathway. However, the adaptors in between
    # (if there are any) can be present or missing. For example, if there are 4 total
    # adaptors in a segment, the 2 adaptors in the middle can be represented by 4 (2^2)
    # possible combinations: both present, one or the other missing, or both missing.
    # However, if there are 3 or more adaptors in the middle, not every combination
    # will be valid because there can never be 3 or more consecutive adaptors that are
    # missing (due to the rule that the delta between consecutive adaptors cannot be
    # more than 3). For 3 adaptors, there will be 8 (2^3) possible combinations but 1
    # combination (where they are all misisng) will invalid and will have to be subtracted.
    # NOTE: I've derived experimentally the number of invalid combinations to subtract
    # from the total possible combinations for when the number of adaptors is between
    # 3 and 8. However, I have not yet determined the formula to calculate the number.
    subtract = {0: 0, 1: 0, 2: 0, 3: 1, 4: 3, 5: 8, 6: 20, 7: 47, 8: 107}
    nums.insert(0, 0)
    start = 0
    total_combinations = 1
    for i in range(0, len(nums)-1):
        if nums[i] + 3 == nums[i+1]:
            segment = nums[start:i+1]
            num_middle_adaptors = len(segment) - 2 if len(segment) > 2 else 0
            combinations = (2**num_middle_adaptors) - subtract[num_middle_adaptors]
            total_combinations *= combinations
            start = i + 1
    return total_combinations

if __name__ == '__main__':
    nums = list(int(line) for line in re.split("\n", sys.stdin.read().rstrip()))
    nums.sort()
    nums.append(nums[-1] + 3)

    part1 = part_1(nums)
    print("PART 1:", part1)

    part2 = part_2(nums)
    print("PART 2:", part2)
