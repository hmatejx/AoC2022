from alive_progress import alive_bar

_magic = 1
APPLY_MAGIC=True

class Monkey:
    # "public"
    number = 0
    items = None
    # "private"
    _inspected = 0
    _next = None
    _a, _b, _c = 0, 0, 0
    _divisible = 0

    def __init__(self, number):
        self.number = number
        self.items = []
        self._next = {}

    def inspect(self):
        self._inspected += 1
        if self._c > 0:
            self.items[0] *= self.items[0]
        elif self._b > 0:
            self.items[0] *= self._b
        else:
            self.items[0] += self._a

    def bored(self):
        self.items[0] = self.items[0] // 3

    def throw(self):
        self._next[self.items[0] % self._divisible == 0].items.append(self.items[0] % _magic if APPLY_MAGIC else self.items[0])
        del self.items[0]

    def print(self):
        print("Monkey {}:".format(self.number))
        print("  Items: {}".format(self.items))
        print("  Operation: new = {}, {}, {}".format(self._c, self._b, self._a))
        print("  Test: divisible by {}".format(self._divisible))
        print("    If true: throw to monkey {}".format(self._next[True].number))
        print("    If false: throw to monkey {}".format(self._next[False].number))
        print("  Inspected: {}".format(self._inspected))

def setup(filename):
    global _magic
    monkeys = []
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
        i = 0
        for line in (line for line in lines if 'Monkey' in line):
            monkeys.append(Monkey(i := i + 1))
        i = 0
        for line in lines:
            if len(line) == 0:
                i += 1
            if 'Starting' in line:
                monkeys[i].items = [int(item.rstrip(',')) for item in line.split()[2:]]
            if 'Operation' in line:
                f = line.split()[3:]
                monkeys[i]._c = 1 if f[0] == 'old' and f[2] == 'old' else 0
                monkeys[i]._b = int(f[2]) if f[0] == 'old' and f[1] == '*' and f[2] != 'old' else 0
                monkeys[i]._a = int(f[2]) if f[0] == 'old' and f[1] == '+' and f[2] != 'old' else 0
            if 'Test' in line:
                monkeys[i]._divisible = int(line.split()[3])
                _magic *= monkeys[i]._divisible
            if 'throw' in line:
                monkeys[i]._next['true' in line] = monkeys[int(line[-1])]
    return monkeys

def monkey_bussiness(monkeys):
    inspections = [monkey._inspected for monkey in monkeys]
    inspections.sort(reverse=True)
    print("{} x {}".format(inspections[0], inspections[1]))
    return inspections[0]*inspections[1]

# Part 1
monkeys = setup("input.txt")
nrounds = 20
with alive_bar(total = nrounds) as bar:
    for round in range(0, nrounds):
        for monkey in monkeys:
            while len(monkey.items):
                monkey.inspect()
                monkey.bored()
                monkey.throw()
        bar()
print("Part 1: {}".format(monkey_bussiness(monkeys)))

# Part 2
monkeys = setup("input.txt")
nrounds = 10000
with alive_bar(total = nrounds) as bar:
    for round in range(0, nrounds):
        for monkey in monkeys:
            while len(monkey.items):
                monkey.inspect()
                monkey.throw()
        bar()
    print("{}: ".format(nrounds), end='')
print("Part 2: {}".format(monkey_bussiness(monkeys)))
