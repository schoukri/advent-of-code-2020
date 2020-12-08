import sys, re, copy

def main():

    ops = list()
    for line in re.split("\n", sys.stdin.read().rstrip()):
        matches = re.match("([a-z]{3}) ([+-]\d+)", line)
        ops.append([matches.group(1), int(matches.group(2))])

    part1 = run(ops)
    print("PART 1:", part1["accumulator"])

    switch = {"jmp": "nop", "nop": "jmp"}
    for i in range(len(ops)):
        op = ops[i][0]
        if op == "acc":
            continue

        ops_copy = copy.deepcopy(ops)
        ops_copy[i][0] = switch[op]
        result = run(ops_copy)
        if result["valid"] == True:
            print("PART 2:", result["accumulator"])
            break



def run(ops):
    i = 0
    result = {"accumulator": 0, "valid": False}
    seen = dict()
    while True:
        if i >= len(ops):
            result["valid"] = True
            return result
        if i in seen:
            return result
        else:
            seen[i] = True

        (op, val) = ops[i]
        if op == "acc":
            result["accumulator"] += val
            i += 1
        elif op == "jmp":
            i += val
        elif op == "nop":
            i += 1


if __name__ == '__main__':
    main()
