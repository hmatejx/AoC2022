from math import ceil
from alive_progress import alive_bar

with open('input.txt') as file:
    blueprints = [[[int(l[6])], [int(l[12])], [int(l[18]), int(l[21])], [int(l[27]), int(l[30])]] \
                   for l in [line.rstrip().split() for line in file]]

def next_steps(blueprint, state):
    next_states = []
    # check which robots can be made
    for r in range(4):
        res, rob, req = state[0:4], state[4:8], blueprint[r]
        # check if we have the prerequisite robots
        if r > 0 and rob[r - 1] == 0:
            continue
        # check if we need this robot (more than max requirement won't help)
        if (r == 0 and rob[0] >= max(blueprint, key=lambda x: x[0])[0]) or (r >= 1 and r <= 2 and rob[r] >= blueprint[r + 1][1]):
            continue
        # calculate time when sufficient resources
        time = max((req[0] - res[0]) / rob[0], 0)
        if r >= 2:
            time = max(time, (req[1] - res[r - 1]) / rob[r - 1])
        time = int(ceil(time)) + 1
        # update state (generate resources, build robot if remaining time permits)
        newstate = state.copy()
        if time <= state[-1]:
            newstate[r + 4] += 1
            newstate[0] -= req[0]
            if r >= 2:
                newstate[r - 1] -= req[1]
        else:
            time = state[-1]
        for i in range(4):
            newstate[i] += rob[i]*time
        newstate[-1] -= time
        next_states.append(newstate)

    return next_states

def score(blueprint, remaining=24):
    #        resources               robots
    #        ore clay obsidian geode ore clay obsidian geode
    state = [0,  0,   0,       0,    1,  0,   0,       0,    remaining]
    front = [state]
    best_state = state
    while front:
        state = front.pop(0)
        for s in next_steps(blueprint, state):
            if s[3] > best_state[3]:
                best_state = s
            # if time left, and if high estimate of possible score larger than the current best score
            if s[8] > 0 and (s[3] + s[7]*s[8] + sum(range(s[8])) > best_state[3]):
                front.append(s)
    return best_state

with alive_bar(len(blueprints)) as bar:
    scores = []
    for id in range(len(blueprints)):
        res = score(blueprints[id])
        scores.append((id + 1) * res[3])
        bar()
print("Part 1: {}".format(sum(scores)))

with alive_bar(min(len(blueprints), 3)) as bar:
    scores = []
    for id in range(min(len(blueprints), 3)):
        res = score(blueprints[id], 32)
        scores.append(res[3])
        bar()
print("Part 2: {}".format(scores[0]*scores[1]*scores[2]))
