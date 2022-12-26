def scan(input, xr, buffer=False):
    global ground, xmin, xmax, ymax, nx, ny
    # first pass
    veins = []
    xmin, xmax, ymax = 10000, -10000, -10000
    for line in open(input):
        parts =[[int(x), int(y)] for x, y in [part.split(',') for part in line.rstrip().split(' -> ')]]
        veins.append(parts)
        for part in parts:
            if part[0] < xmin: xmin = part[0]
            if part[0] > xmax: xmax = part[0]
            if part[1] > ymax: ymax = part[1]
    if buffer:
        xmin = xr - ymax - 3
        xmax = xr + ymax + 3
        nx = 2*ymax + 7
        ymax += 2
    else:
        xmin -= 1
        xmax += 1
        nx = xmax - xmin + 1
    ny = ymax + 1
    # second pass
    ground = [['.']*nx for y in range(ny)]
    for vein in veins:
        x0, y0 = vein[0]
        ground[y0][x0 - xmin] = '#'
        for i in range(1, len(vein)):
            x1, y1 = vein[i]
            if x1 == x0 and y1 != y0:      # vein moves in y direction
                start, stop = (y0, y1 + 1) if y1 > y0 else (y1, y0 + 1)
                for y in range(start, stop):
                    ground[y][x1 - xmin] = '#'
                y0 = y1
            if y1 == y0 and x1 != x0:      # vein moves in x direction
                start, stop = (x0, x1 + 1) if x1 > x0 else (x1, x0 + 1)
                for x in range(start, stop):
                    ground[y1][x - xmin] = '#'
                x0 = x1
    ground[0][xr - xmin] = '+'
    if buffer:
        for x in range(xmin, xmax + 1):
            ground[ymax][x - xmin] = '#'

def paint():
    xl = ['{:>3}'.format(x) for x in range(xmin, xmax + 1)]
    for hl in range(len(str(xmax))):
        print('    ' + ''.join([l[hl] for l in xl]))
    for y in range(ny):
        print('{:>3} '.format(y) + ''.join([ground[y][x] for x in range(nx)]))

def pour():
    while True:
        x0 = 500 - xmin
        x, y = x0, 0
        while y + 1 <= ymax:
            # flow down as far as you can
            if ground[y + 1][x] == '.':
                y += 1
            # we hit ground or sand
            else:
                # check if we can flow left
                if ground[y + 1][x - 1] == '.':
                    x -= 1
                    y += 1
                # check if we can flow right
                elif ground[y + 1][x + 1] == '.':
                    x += 1
                    y += 1
                # we came to a stop
                else:
                    ground[y][x] = 'o'
                    break
        # check if sand is falling into the endless void
        if y + 1 > ymax or y == 0:
            break

# initialize the scan, do not include buffer
scan('input.txt', xr=500)
pour()
print("Part 1: {}".format(sum([sum([c == 'o' for c in line]) for line in ground])))
paint()

# reinitialize the scan, this time add a buffer
scan('input.txt', xr=500, buffer=True)
pour()
print("Part 2: {}".format(sum([sum([c == 'o' for c in line]) for line in ground])))
paint()