from functools import cmp_to_key

with open('input.txt') as file:
    lines = [line.rstrip() for line in file]
    pairs = []
    left, right = None, None
    for line in lines:
        if left is None: left = eval(line)
        elif left is not None and right is None: right = eval(line)
        if len(line) == 0:
            pairs.append([left, right])
            left, right = None, None
    pairs.append([left, right])

def compare(left, right):
    # both values are integers, recursion should end here
    if (not type(left) == list) and (not type(right) == list):
        if left == right:
            return 0
        elif left < right:
            return 1
        else:
            return -1
    # both values are lists
    if type(left) == list and type(right) == list:
        for i in range(max(len(left), len(right))):
            if i == len(left) and i < len(right):
                return 1
            if i == len(right) and i < len(left):
                return -1
            comp = compare(left[i], right[i])
            if comp == -1:
                return -1
            if comp == 1:
                return 1
        return 0
    # exactly one value is an integer
    if type(left) == list and (not type(right) == list):
        return compare(left, [right])
    if type(right) == list and (not type(left) == list):
        return compare([left], right)

res1 = [i + 1 for i in range(len(pairs)) if compare(pairs[i][0], pairs[i][1]) == 1]
print("Part 1: {}".format(sum(res1)))

packets = [[[2]], [[6]]]
for line in lines:
    if len(line) > 0:
        packets.append(eval(line))
packets.sort(key = cmp_to_key(compare))
packets.reverse()
res2 = [i + 1 for i in range(len(packets)) if packets[i] == [[2]] or packets[i] == [[6]]]
print("Part 2: {}".format(res2[0]*res2[1]))
