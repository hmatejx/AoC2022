with open('input.txt') as file:
    lines = [line.rstrip().split(',') for line in file]
    assignments = [[list(map(int, r1.split('-'))),  list(map(int, r2.split('-')))] for r1, r2 in lines]

res1 = res2 = 0
for a1, a2 in assignments:
    # check if contained
    if (a1[0] <= a2[0] and a1[1] >= a2[1]) or (a2[0] <= a1[0] and a2[1] >= a1[1]):
        res1 += 1
    # check if overlapping
    if a2[0] <= a1[1] and a2[1] >= a1[0]:
        res2 += 1

print("Part 1: {}".format(res1))
print("Part 2: {}".format(res2))
