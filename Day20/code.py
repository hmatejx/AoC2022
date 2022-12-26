from alive_progress import alive_bar

with open('test.txt') as file:
    numbers = [int(line) for line in file]

class Node:
    def __init__(self, v, i):
        self.v = v
        self.i = i
        self.prev = None
        self.next = None

class Circular:
    def __init__(self, values):
        self.head = None
        for i, v in enumerate(values):
            self.append(Node(v, i))
        self.len = len(values)

    def insert_after(self, ref_node, new_node):
        new_node.prev = ref_node
        new_node.next = ref_node.next
        new_node.next.prev = new_node
        ref_node.next = new_node

    def append(self, new_node):
        if self.head is None:
            self.head = new_node
            new_node.next = new_node
            new_node.prev = new_node
        else:
            self.insert_after(self.head.prev, new_node)

    def print(self, reverse=False):
        if self.head is not None:
            node = self.head
            while True:
                print('{}({})'.format(node.v, node.i), end=' ')
                node = node.next if not reverse else node.prev
                if node == self.head:
                    break
            print()

    def findnode(self, idx):
        node = self.head
        while node.i != idx:
            node = node.next
        return node

    def move(self, idx):
        node_to_move = self.findnode(idx)
        dist = node_to_move.v % (self.len - 1)
        if dist == 0:
            return
        if node_to_move == self.head:
            self.head = node_to_move.next
        node = node_to_move
        for i in range(dist):
            node = node.next
        node_to_move.next.prev = node_to_move.prev
        node_to_move.prev.next = node_to_move.next
        node_to_move.prev = node
        node_to_move.next = node.next
        node.next.prev = node_to_move
        node.next = node_to_move

    def afterzero(self, i):
        dist = i % self.len
        node = self.head
        while node.v != 0:
            node = node.next
        for i in range(dist):
            node = node.next
        return node.v

    def grove(self):
        return sum([self.afterzero(1000), self.afterzero(2000), self.afterzero(3000)])

# Part 1
mixer = Circular(numbers)
for i, n in enumerate(numbers):
    mixer.move(i)
print("Part 1: {}".format(mixer.grove()))

# Part 2
mixer = Circular([n*811589153 for n in numbers])
with alive_bar(10) as bar:
    for round in range(10):
        for i, n in enumerate(numbers):
            mixer.move(i)
        bar()
print("Part 2: {}".format(mixer.grove()))

mixer.print()
