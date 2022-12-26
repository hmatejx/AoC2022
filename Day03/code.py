def priority(item):
    return ord(item) - ord('a') + 1 if item.islower() else ord(item) - ord('A') + 27

sum_priority = sum_badge = 0
with open('input.txt') as file:
    lines = [line.rstrip() for line in file]
    groups = []
    for line in lines:
        mid = int(len(line)/2)
        left, right = list(line[0:mid]), list(line[mid:])
        groups.append(list(line))
        item = set(left).intersection(set(right)).pop()
        sum_priority += priority(item)
    for i in range(0, int(len(groups)/3)):
        badge = set(groups[3*i]).intersection(set(groups[3*i + 1]).intersection(set(groups[3*i + 2]))).pop()
        sum_badge += priority(badge)

print("Part 1: {}".format(sum_priority))
print("Part 2: {}".format(sum_badge))
