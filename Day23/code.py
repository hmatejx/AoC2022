from alive_progress import alive_bar
from sortedcontainers import SortedList

with open('input.txt') as file:
    lines = [line.rstrip() for line in file]

elves = []
for j in range(len(lines)):
    for i in range(len(lines[0])):
        if lines[j][i] == '#':
            elves.append((i, j))
nelves = len(elves)

north, south, west, east = (0, -1), (0, 1), (-1, 0), (1, 0)
directions = [north, south, west, east]
#              E     NE       N       NW      W      SW       S     SE
neighbors = (east, (1, -1), north, (-1, -1), west, (-1, 1), south, (1, 1))

def bounding_box():
    xmin, xmax = min(list(zip(*elves))[0]), max(list(zip(*elves))[0])
    ymin, ymax = min(list(zip(*elves))[1]), max(list(zip(*elves))[1])
    return xmin, xmax, ymin, ymax

def plot():
    xmin, xmax, ymin, ymax = bounding_box()
    for y in range(ymin - 1, ymax + 2):
        line = ''.join('#' if (x, y) in elves else '.' for x in range(xmin - 1, xmax + 2))
        print(line)

k = 0
with alive_bar() as bar:
    while True:
        k += 1
        move = [False]*nelves
        proposals = elves.copy()
        selves = SortedList(elves)
        for i in range(nelves):
            elf = elves[i]
            n = tuple((elf[0] + n[0], elf[1] + n[1]) in selves for n in neighbors)
            if not any(n):
                continue
            for j in range(4):
                d = directions[j]
                if d == north and not any(n[1:4]):
                    proposals[i] = elf[0] + north[0], elf[1] + north[1]
                    move[i] = True
                elif d == south and not any(n[5:8]):
                    proposals[i] = elf[0] + south[0], elf[1] + south[1]
                    move[i] = True
                elif d == west and not any(n[3:6]):
                    proposals[i] = elf[0] + west[0], elf[1] + west[1]
                    move[i] = True
                elif d == east and not (any(n[0:2]) or n[7]):
                    proposals[i] = elf[0] + east[0], elf[1] + east[1]
                    move[i] = True
                if move[i]:
                    break
        if not any(move):
            break
        sproposals = SortedList(proposals)
        for i in range(nelves):
            pi = proposals[i]
            sproposals.remove(pi)
            if move[i] is None or pi in sproposals:
                sproposals.add(pi)
                continue
            sproposals.add(pi)
            elves[i] = pi
        directions = directions[1:] + [directions[0]]
        bar()
        if k == 10:
            xmin, xmax, ymin, ymax = bounding_box()
            print("Part 1: {}".format((xmax - xmin + 1)*(ymax - ymin + 1) - nelves))
print("Part 2: {}".format(k))
