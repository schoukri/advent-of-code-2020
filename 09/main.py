import sys, re

def part_1(nums, preamble):
    def find(n):
        for a in range(n - preamble, n):
            for b in range(a + 1, n):
                if nums[a] + nums[b] == nums[n]:
                    return True
        return False
    for i in range(preamble, len(nums)):
        if not find(i):
            return nums[i]

def part_2(nums, target):
    for i in range(len(nums) - 1):
        total = nums[i]
        for j in range(i + 1, len(nums)):
            total += nums[j]
            if total == target:
                group = list(map(lambda x: nums[x], range(i, j + 1)))
                return min(group) + max(group)
            elif total > target:
                break
    return -1

if __name__ == '__main__':
    nums = list(int(line) for line in re.split("\n", sys.stdin.read().rstrip()))

    part1 = part_1(nums, 25)
    print("PART 1:", part1)

    part2 = part_2(nums, part1)
    print("PART 2:", part2)
