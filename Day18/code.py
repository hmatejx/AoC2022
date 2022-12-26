with open('input.txt') as file:
    lines = [eval('(' + line.rstrip() + ')')  for line in file]
    cubes = {}
    for cube in lines:
        cubes[cube] = 1

xmin, xmax = min(list(zip(*lines))[0]), max(list(zip(*lines))[0])
ymin, ymax = min(list(zip(*lines))[1]), max(list(zip(*lines))[1])
zmin, zmax = min(list(zip(*lines))[2]), max(list(zip(*lines))[2])

def area():
    area = 0
    for x, y, z in lines:
        area += 1 if cubes.get((x+1, y, z)) is None else 0
        area += 1 if cubes.get((x-1, y, z)) is None else 0
        area += 1 if cubes.get((x, y+1, z)) is None else 0
        area += 1 if cubes.get((x, y-1, z)) is None else 0
        area += 1 if cubes.get((x, y, z+1)) is None else 0
        area += 1 if cubes.get((x, y, z-1)) is None else 0
    return area

def in_box(x, y, z):
    return x >= xmin and x <= xmax and y >= ymin and y <= ymax and z >= zmin and z <= zmax

def flood_fill(start):
    filled = {}
    filled[start] = -1
    neigh = (0, 0, -1), (0, 0, 1), (0, -1, 0), (0, 1, 0), (-1, 0, 0), (1, 0, 0)
    frontier = [start + (0, )]
    while frontier:
        f = min(frontier, key=lambda f: f[3])
        frontier.remove(f)
        for n in neigh:
            pos = f[0] + n[0], f[1] + n[1], f[2] + n[2]
            if (not filled.get(pos)) and (not cubes.get(pos)) and in_box(*pos):
                frontier.append(pos + (f[3] + 1, ))
                filled[pos] = f[3] + 1
    return filled

print("Part 1: {}".format(area()))

# fill bounding box with water
filled = flood_fill((xmin, ymin, zmin))
# then fill holes
for x in range(xmin, xmax + 1):
    for y in range(ymin, ymax + 1):
        for z in range(zmin, zmax + 1):
            if (not filled.get((x, y, z))) and (not cubes.get((x, y, z))):
                cubes[(x, y, z)] = 0

print("Part 2: {}".format(area()))
