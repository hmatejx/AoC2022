# read elf data
elfs = []
with open('input.txt') as f:
    lines = [line.rstrip() for line in f]
    food = []
    for l in lines:
        if l == '':
            elfs.append(food)
            food = []
        else:
            food.append(int(l))

# calculate total calories
cals = [sum(cal) for cal in elfs]
cals.sort(reverse=True)

print("Part 1: {}".format(cals[0]))
print("Part 2: {}".format(sum(cals[0:3])))