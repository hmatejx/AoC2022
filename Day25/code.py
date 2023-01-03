with open('input.txt') as file:
    lines = [line.rstrip() for line in file]

def from_snafu(x):
    r = 0
    for i in range(len(x)):
        q = x[len(x) - 1 - i]
        d = 0
        if q in ('2', '='):
            d = 2 if q == '2' else -2
        elif q != '0':
            d = 1 if q == '1' else -1
        r += d*(5**i)
    return r

def to_snafu(x):
    i, r, sign, s = 0, 0, 1, ''
    while True:
        r += 2*(5**i)
        if r >= x:
            break
        i += 1
    for j in range(i, -1, -1):
        r = 5**j
        if x <= 2*r/5:
            s += '0'
            continue
        two = abs(x - 2*r) < abs(x - r)
        s += ('2' if sign == 1 else '=') if two else ('1' if sign == 1 else '-')
        x -= 2*r if two else r
        sign = sign * (-1 if x < 0 else 1)
        x = abs(x)
    return s

res1 = sum([from_snafu(x) for x in lines])
print("Part 1: {}".format(to_snafu(res1)))
