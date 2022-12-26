map = []
with open('input.txt') as file:
    for line in [line.rstrip() for line in file]: 
        map.append([int(c) for c in line])

dimx, dimy = len(map), len(map[0])
visible = [[0]*dimx for i in range(dimy)]
scores =[[0]*dimx for i in range(dimy)]

def isvisible(i, j):
    if i == 0 or i == dimx - 1 or j == 0 or j == dimy - 1:
        return 1
    if max(map[i][0:j]) < map[i][j] or max(map[i][j+1:dimy]) < map[i][j]:
        return 1
    smaller = True
    for ii in range(0, i):
        if map[ii][j] >= map[i][j]:
            smaller = False
            break
    if smaller:
        return 1
    smaller = True
    for ii in range(i+1, dimx):
        if map[ii][j] >= map[i][j]:
            smaller = False
            break
    if smaller:
        return 1
    return 0

def score(i, j):
    up, down, left, right = 0, 0, 0, 0
    for ii in range(1, i+1):
        up = up + 1
        if map[i-ii][j] >= map[i][j]:
            break
    for ii in range(i+1, dimy):
        down = down + 1
        if map[ii][j] >= map[i][j]:
            break
    for jj in range(1, j+1):
        left = left + 1
        if map[i][j-jj] >= map[i][j]:
            break
    for jj in range(j+1, dimx):
        right = right + 1
        if map[i][jj] >= map[i][j]:
            break
    return(left*right*up*down)

for i in range(dimx):
    for j in range(dimy):
        visible[i][j] = isvisible(i, j)
        scores[i][j] = score(i, j)

print("Part 1: {}".format(sum(sum(x) for x in visible)))
print("Part 2: {}".format(max(max(s) for s in scores)))
