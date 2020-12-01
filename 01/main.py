import sys

nums = []
for line in sys.stdin:
    nums.append(int(line.rstrip()))

for i in range(0, len(nums)):
    for j in range(i+1, len(nums)):
        if nums[i] + nums[j] == 2020:
            print("PART 1: {}".format(nums[i] * nums[j]))
        for k in range(j+1, len(nums)):
            if nums[i] + nums[j] + nums[k]== 2020:
                print("PART 2: {}".format(nums[i] * nums[j] * nums[k]))
