x = [1]
cycle = 0
nrow, ncol = 6, 40
crt = [['.']*ncol for i in range(nrow)]

def run_cycle(add=None):
    global cycle
    # first, update cycle counter
    cycle += 1
    # second, update crt
    col = (cycle - 1) % ncol
    row = (cycle - 1) // ncol
    sprite = x[-1]
    if abs(sprite - col) <= 1:
        crt[row][col] = '#'
    for line in crt:
        print(''.join(line))
    print()
    # last, update register history
    x.append(x[-1] if add is None else x[-1] + add)

with open('input.txt') as file:
    lines = [line.rstrip() for line in file]
    for cmd in [line.split(' ') for line in lines]:
        run_cycle()                               # addx or noop
        if len(cmd) > 1: run_cycle(int(cmd[1]))   # addx 2nd cycle

print('Part 1: {}'.format(sum([i*x[i-1] for i in [20, 60, 100, 140, 180, 220]])))
print('Part 2: <see console output>')
