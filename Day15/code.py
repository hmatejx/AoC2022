from alive_progress import alive_bar

def dist(x0, y0, x1, y1):
    return abs(x0 - x1) + abs(y0 - y1)

with open('input.txt') as file:
    lines = [line.rstrip().split() for line in file]
    sensors = [[int(line[2][2:-1]), int(line[3][2:-1])] for line in lines]
    beacons = [[int(line[8][2:-1]), int(line[9][2:])] for line in lines]
    for i in range(len(sensors)):
        sensors[i] += [dist(*sensors[i][0:2], *beacons[i][0:2])]

def intersect(sensor, yr):
    x, y, r = sensor
    dy = abs(y - yr)
    if dy > r:
        return None
    dx = r - dy
    return [x - dx, x + dx]

def overlapping(a1, a2):
    if (min(a2) - 1 > max(a1)) or (min(a1) - 1> max(a2)):
        return 0
    return 1

def scan_row(yr):
    covered = []
    for sensor in sensors:
        r = intersect(sensor, yr)
        if r is not None:
            covered.append(r)
    covered.sort(key = lambda x: x[1] - x[0], reverse=True)
    while True:
        o = [i+1 for i in range(len(covered)-1) if overlapping(covered[0], covered[i+1])]
        merged = covered[0]
        for i in o:
            merged = [min(merged[0], covered[i][0]), max(merged[1], covered[i][1])]
        covered = [covered[i] for i in range(1, len(covered)) if i not in o]
        covered.append(merged)
        if len(o) == 0:
            break
    return covered

print("Part 1: {}".format(sum(map(lambda x: x[1] - x[0], scan_row(2000000)))))

with alive_bar(4000000) as bar:
    for yr in range(4000000):
        covered = scan_row(yr)
        if len(covered) > 1:
            covered.sort(key = lambda x: x[0])
            print("Part 2: {}".format(yr + 4000000*(covered[0][1] + 1)))
        bar()
