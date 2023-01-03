with open('input.txt') as file:
    valley = [line.rstrip()[1:-1] for line in file][1:-1]
    dimx, dimy = len(valley[0]), len(valley)
    begin=(0, -1)
    end=(dimx - 1, dimy)

def walk(begin, end, time):
    pos = set([begin])
    i = time
    while True:
        i += 1
        newpos = set()
        for x, y in pos:
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1), (x, y)):
                # check if at end
                if nx == end[0] and ny == end[1]:
                    return i
                # check for boundearies
                if (nx < 0 or nx >= dimx or ny < 0 or ny >= dimy):
                    continue
                # check for blizzards
                if    valley[ny][(nx + i) % dimx] == '<' \
                   or valley[ny][(nx - i) % dimx] == '>' \
                   or valley[(ny + i) % dimy][nx] == '^' \
                   or valley[(ny - i) % dimy][nx] == 'v':
                    continue
                newpos.add((nx, ny))
        if newpos:
            pos = newpos

res1 = walk(begin, end, 0)
print("Part 1: {}".format(res1))

res2 = walk(begin, end, walk(end, begin, res1))
print("Part 2: {}".format(res2))
