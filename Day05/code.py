from copy import deepcopy

def move1(op, stack):
    q, fr, to = op
    for i in range(0, q):
        stack[to - 1].append(stack[fr - 1].pop())

def move2(op, stack):
    q, fr, to = op
    from_stack = stack[fr - 1]
    stack[to - 1].extend(from_stack[len(from_stack)-q:])
    del from_stack[len(from_stack)-q:]

instructions, stack1 = [], []
with open('input.txt') as file:
    lines = [line.rstrip('\n') for line in file.readlines()]
    instruction_part = False
    for line in lines:
        if len(line) == 0:        # skip empty line
            continue
        if instruction_part:      # read in the instruction
            instructions.append(list(map(int, map(line.split(" ").__getitem__, [1, 3, 5]))))
        else:                     # read in the stack state
            stack1.append([line[i:i+4].strip(" []") for i in range(0, len(line), 4)])
            if line[1:2] == '1':  # beginning of stack header
                instruction_part = True

stack1 = [list(x)[::-1] for x in zip(*stack1)]  # transpose the stack and remove empty elements
stack1 = [[y for y in x if y != ''] for x in stack1]
stack2 = deepcopy(stack1)

for op in instructions: # perform all moves on the stacks
    move1(op, stack1)
    move2(op, stack2)

res1 = ''.join([x[-1] for x in stack1 if len(x) > 0])
res2 = ''.join([x[-1] for x in stack2 if len(x) > 0])
print("Part1: {}".format(res1))
print("Part2: {}".format(res2))