import networkx as nx

def setup(filename):
    monkeys, edges, lines = {}, [], [line.rstrip().split() for line in open(filename)]
    for line in lines:
        if len(line) == 2:
            monkey = {'value': int(line[1])}
        else:
            monkey = {'sources': [line[1], line[3]], 'inputs': None, 'value': None}
            if  line[2] == '+':   monkey['eval'] = lambda x, y: x + y
            elif line[2] == '-':  monkey['eval'] = lambda x, y: x - y
            elif line[2] == '*':  monkey['eval'] = lambda x, y: x * y
            elif line[2] == '/':  monkey['eval'] = lambda x, y: x / y
            edges.extend([[line[1], line[0][0:4]], [line[3], line[0][0:4]]])
        monkeys[line[0][0:4]] = monkey
    graph = nx.DiGraph()
    graph.add_edges_from(edges)
    return monkeys, list(nx.topological_sort(graph))

def get_to_the_root(humn=None):
    if humn is not None:
        monkeys['humn']['value'] = humn
    for name in path:
        if monkeys[name].get('eval'):
            monkeys[name]['inputs'] = monkeys[monkeys[name]['sources'][0]]['value'], monkeys[monkeys[name]['sources'][1]]['value']
            monkeys[name]['value'] = monkeys[name]['eval'](*monkeys[name]['inputs'])
    return monkeys['root']['value']

monkeys, path = setup('input.txt')
print("Part 1: {:.0f}".format(get_to_the_root()))

# when you figure out the function is a linear function ;D
monkeys['root']['eval'] = lambda x, y: x - y
y2, y1 = get_to_the_root(1000000), get_to_the_root(0)
print("Part 2: {}".format(round(-1000000*y1 / (y2 - y1))))
