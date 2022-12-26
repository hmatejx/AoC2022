def game1(v1, v2):
    if v2 - v1 == -1 or v2 - v1 == 2: return v2   # lose: 21 32 13
    if v1 == v2: return v2 + 3                    # draw: 11 22 33
    return v2 + 6                                 # win: 12 23 31

def game2(v1, v2):
        if v2 == 1: return v1 - 1 if v1 > 1 else 3  # need to lose
        if v2 == 2: return v1 + 3                   # need to draw
        return (v1 + 1 if v1 < 3 else 1) + 6        # need to win

res1, res2 = 0, 0
with open('input.txt') as file:
    lines = [line.rstrip() for line in file]
    for line in lines:
        p1, p2 = line.split(' ')
        v1 = ord(p1) - ord('A') + 1         # Rock, Paper, Scissors -> 1, 2, 3
        v2 = ord(p2) - ord('X') + 1
        res1 += game1(v1, v2)
        res2 += game2(v1, v2)

print("Part 1: {}".format(res1))
print("Part 1: {}".format(res2))
