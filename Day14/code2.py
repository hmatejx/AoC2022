#!/usr/bin/python3
import sys

ground = None
xmin = xmax = ymin = ymax = None
nx = ny = None


def scan(input):
    global ground, xmin, xmax, ymin, ymax, nx, ny
    # first pass
    veins = []
    for line in open(input):
        parts = line.split(', ')
        xp, yp = (parts[0], parts[1]) if parts[0][0] == 'x' else (parts[1], parts[0])
        x, y = list(map(int, xp[2:].split('..'))), list(map(int, yp[2:].split('..')))
        veins.append([x, y])
    xmin, xmax = min(map(lambda v: min(v[0]), veins)) - 1, max(map(lambda v: max(v[0]), veins)) + 1
    ymin, ymax = min(map(lambda v: min(v[1]), veins)), max(map(lambda v: max(v[1]), veins))
    nx = xmax - xmin + 1
    ny = ymax + 1
    # second pass
    ground = [['.']*nx for y in range(ny)]
    for vein in veins:
        for x in range(vein[0][0] - xmin, vein[0][-1] + 1 - xmin):
            for y in range(vein[1][0], vein[1][-1] + 1):
                ground[y][x] = '#'
    ground[0][500 - xmin] = '+'


def paint():
    xl = ['{:>3}'.format(x) for x in range(xmin, xmax + 1)]
    for hl in range(len(str(xmax))):
        print('    ' + ''.join([l[hl] for l in xl]))
    for y in range(ny):
        print('{:>3} '.format(y) + ''.join([ground[y][x] for x in range(nx)]))


def spread(x, y):
    l = r = x
    while ground[y + 1][l] != '.' and ground[y][l] != '#':
        l -= 1
    while ground[y + 1][r] != '.' and ground[y][r] != '#':
        r += 1
    water = '|' if ground[y][l] != '#' or ground[y][r] != '#' else '~'
    for s in range(l + 1, r):
        if ground[y][s] != '#':
            ground[y][s] = water
    if ground[y][l] != '#':
        pour(l, y)
    if ground[y][r] != '#':
        pour(r, y)


def pour(x, y):
    # stop recursion if we reach ymax or hit an existing flow
    if y + 1 > ymax or ground[y + 1][x] == '|':
        ground[y][x] = '|'
        return
    # check if we can continue to go down
    if ground[y + 1][x] == '.':
        ground[y][x] = '|'
        pour(x, y + 1)
        # check if after pouring resulted in standing water
        if ground[y + 1][x] == '~':
            spread(x, y)
    # path down is blocked, we must spread
    elif ground[y + 1][x] == '#' or ground[y + 1][x] == '~':
        spread(x, y)


if __name__ == '__main__':
    scan('input2.txt')
    sys.setrecursionlimit(2000)

    pour(500 - xmin, 1)
    s1 = sum([sum([c == '|' for c in line]) for line in ground[ymin:]])
    s2 = sum([sum([c == '~' for c in line]) for line in ground[ymin:]])
    paint()

    print(s1 + s2) # part1
    print(s2) # part2