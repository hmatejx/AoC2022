nknots = 10
move_head = {'L': (-1, 0), 'R': (1, 0), 'U': (0, 1), 'D': (0, -1)}
knots_path = [{'0,0': 1} for i in range(nknots)]
knots = [[0, 0] for i in range(nknots)]

""" commented parts below just for drawing ...
x0, x1, y0, y1 = [0]*4
def state(knots):
    for y in range(y1, y0 - 1, -1):
        for x in range(x0, x1 + 1):
            if x == 0 and y == 0:
                print('s', end='')
                continue
            empty = True
            for i in range(0, nknots):
                if knots[i][0] == x and knots[i][1] == y:
                    print('H123456789'[i], end = '')
                    empty = False
                    break
            if empty:
                print('.', end='')
        print()

def path(p):
    for y in range(y1, y0 - 1, -1):
        for x in range(x0, x1 + 1):
            if x == 0 and y == 0:
                print('s', end='')
            else:
                s = '#' if p.get('{},{}'.format(x, y)) else '.'
                print(s, end='')
        print()
"""

def sign(x):
    return (x > 0) - (x < 0)

with open('input.txt') as file:
    moves = [[d, int(c)] for d, c in [line.rstrip().split() for line in file]]
    """
    x, y = 0, 0                   # starting point
    for d, c in moves:            # calculate extreme dimensions
        di, dj = move_head[d]
        for k in range(0, c):
            x += di
            y += dj
            if x < x0: x0 = x
            if x > x1: x1 = x
            if y < y0: y0 = y
            if y > y1: y1 = y
    """
    for d, c in moves:
        di, dj = move_head[d]
        for k in range(0, c):
            knots[0][0] += di     # move head
            knots[0][1] += dj
            knots_path[0]['{},{}'.format(*knots[0])] = 1
            for i in range(1, nknots):      # move other knots one by one
                dist_i = knots[i-1][0] - knots[i][0]
                dist_j = knots[i-1][1] - knots[i][1]
                if abs(dist_i) == 2 or abs(dist_j) == 2:
                    delta_i = sign(dist_i)
                    delta_j = sign(dist_j)
                    knots[i][0] += delta_i
                    knots[i][1] += delta_j
                    knots_path[i]['{},{}'.format(*knots[i])] = 1

print('Part 1: {}'.format(len(knots_path[1])))
print('Part 2: {}'.format(len(knots_path[nknots-1])))