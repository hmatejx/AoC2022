import re

with open('input.txt') as file:
    lines = [line.rstrip() for line in file]
    grove = lines[:-2]
    password = re.split('(\d+)',lines[-1])[1:-1]

def plot():
    for j in range(dimy):
        if j != y:
            print(grove[j])
        else:
            print(grove[j][:x] + '>v<^'[facing] + grove[j][x+1:])

# x and y direction boundaries for part 1
dimx, dimy = max(len(line) for line in grove), len(grove)
xbounds = [[50, 149]]*50 + [[50, 99]]*50 + [[0, 99]]*50 + [[0, 49]]*50
ybounds = [[100,199]]*50 + [[0, 149]]*50 + [[0, 49]]*50

# Part 1
x, y, facing = xbounds[0][0], 0, 0
for command in password:
    if command.isnumeric():
        for i in range(int(command)):
            if facing % 2 == 0:
                d = (-1)**(facing // 2)
                xn, yn = x + d, y
                if xn < xbounds[y][0] or xn > xbounds[y][1]:
                    xn = xbounds[y][0] if d == 1 else xbounds[y][1]
            else:
                d = (-1)**((facing - 1) // 2)
                xn, yn = x, y + d
                if yn < ybounds[x][0] or yn > ybounds[x][1]:
                    yn = ybounds[x][0] if d == 1 else ybounds[x][1]
            if grove[yn][xn] == "#":
                break
            x, y = xn, yn
    else:
        facing = (facing + 1) % 4 if command == 'R' else (facing + 3) % 4

print("Part 1: {}".format(1000*(y + 1) + 4*(x + 1) + facing))

# Part 2
# face mapping for part 2, doesn't work for the test due to different cube face mapping :(
dim = len(grove[0]) // 3
face = [' '*dim + '1'*dim + '2'*dim for i in range(dim)] +\
       [' '*dim + '3'*dim + ' '*dim for i in range(dim)] +\
       ['4'*dim + '5'*dim + ' '*dim for i in range(dim)] +\
       ['6'*dim + ' '*dim + ' '*dim for i in range(dim)]

x, y, facing = xbounds[0][0], 0, 0
for command in password:
    if command.isnumeric():
        for i in range(int(command)):
            dx, dy = (-1)**(facing // 2) if facing % 2 == 0 else 0, (-1)**((facing - 1) // 2) if facing % 2 == 1 else 0
            xn, yn, facingn = x + dx, y + dy, facing
            if face[y][x] == '1':
                if xn == dim-1:       # wrap to face 4 and switch facing
                    xn, yn, facingn = 0, 3*dim - y - 1, 0
                elif yn == -1:        # wrap to face 6 and switch facing
                    xn, yn, facingn = 0, x + 2*dim, 0
            if face[y][x] == '2':
                if xn == 3*dim:       # wrap to face 5 and switch facing
                    xn, yn, facingn = 2*dim - 1, 3*dim - y - 1, 2
                elif yn == -1:        # wrap to face 6
                    xn, yn = x - 2*dim, 4*dim-1
                elif yn == dim:       # wrap to face 3 and switch facing
                    xn, yn, facingn = 2*dim - 1, x - dim, 2
            if face[y][x] == '3':
                if xn == dim - 1:     # wrap to face 4 and switch facing
                    xn, yn, facingn = y - dim, 2*dim, 1
                elif xn == 2*dim:     # wrap to face 2 and switch facing
                    xn, yn, facingn = dim + y, dim - 1, 3
            if face[y][x] == '4':
                if xn == -1:          # wrap to face 1 and switch facing
                    xn, yn, facingn = dim, 3*dim - 1 - y, 0
                elif yn == 2*dim - 1:  # wrap to face 3 and switch facing
                    xn, yn, facingn = dim, x + dim, 0
            if face[y][x] == '5':
                if xn == 2*dim:       # wrap to face 2 and switch facing
                    xn, yn, facingn = 3*dim - 1, 3*dim - y - 1, 2
                elif yn == 3*dim:     # wrap to face 6 and switch facing
                    xn, yn, facingn = dim - 1, x + 2*dim, 2
            if face[y][x] == '6':
                if xn == -1:           # wrap to face 1 and switch facing
                    xn, yn, facingn = y - 2*dim, 0, 1
                elif xn == dim:        # wrap to face 4 and switch facing
                    xn, yn, facingn = y - 2*dim, 3*dim - 1, 3
                elif yn == 4*dim:      # wrap to face 2
                    xn, yn = x + 2*dim, 0
            if grove[yn][xn] == "#":
                break
            x, y, facing = xn, yn, facingn
    else:
        facing = (facing + 1) % 4 if command == 'R' else (facing + 3) % 4

print("Part 2: {}".format(1000*(y + 1) + 4*(x + 1) + facing))
