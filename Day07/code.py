listing, dir = [], ''
with open('input.txt') as file:
    for line in [line.rstrip() for line in file]: 
        if line == '$ ls': 
            continue
        if line[0:7] == '$ cd ..':
            dir = dir[0:dir[:-1].rfind('/') +1]
        elif line[0:4]== '$ cd':
            dir = dir + line[5:] + '/' if line[5] != '/' else '/'
        else:
            listing.append([dir] + line.split(' ')[::-1])

sizes = {}
for dir, size in [[d, int(s)] for d, _, s in listing if s.isnumeric()]:
    sizes[dir] = sizes[dir] + size if sizes.get(dir) else size
    while dir != '/':  # update the size of parent directiories
        dir = dir[0:dir[:-1].rfind('/')+1]
        sizes[dir] = sizes[dir] + size if sizes.get(dir) else size
sizes2 = [[k, v] for k, v in sizes.items() if 70000000 - sizes['/'] + v > 30000000]

print("Part 1: {}".format(sum([s for s in sizes.values() if s <= 100000])))
print("Part 2: {}".format(min(d for _, d in sizes2)))
