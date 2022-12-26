import pprint

def setup(file):
    with open(file) as file:
        lines = [line.rstrip() for line in file]
        # create nodes and connections
        nodes = {}
        for line in [line.split() for line in lines]:
            nodes[line[1]] = {'flow': int(line[4][5:-1])}
            next = {}
            for neigh in [n.rstrip(',') for n in line[9:]]:
                next[neigh] = 1
            nodes[line[1]]['next'] = next
        # remove flow 0 nodes
        to_remove = [n for n in nodes if nodes[n]['flow'] == 0 and n != 'AA']
        for rem in to_remove:
            next = nodes[rem]['next']
            for n1 in next:
                for n2 in [n for n in next if n != n1]:
                    nodes[n1]['next'][n2] = nodes[rem]['next'][n1] + nodes[rem]['next'][n2]
            for n in next:
                del nodes[n]['next'][rem]
            del nodes[rem]
        # adjacency matrix
        INF = 10000
        N = len(nodes)
        names = list(nodes.keys())
        names.sort(key = lambda x: nodes[x]['flow'], reverse=True)  # sort nodes by descending flow
        G = [[INF,]*N for i in range(N)]
        for i in range(N):
            for j in range(N):
                if i == j:
                    G[i][j] = 0
                elif nodes[names[i]]['next'].get(names[j]):
                    G[i][j] = nodes[names[i]]['next'][names[j]]
        # node distance (Floyd-Warshall)
        dist = list(map(lambda p: list(map(lambda q: q, p)), G))
        for r in range(len(G)):
            for p in range(len(G)):
                for q in range(len(G)):
                    dist[p][q] = min(dist[p][q], dist[p][r] + dist[r][q])
        return dist, names, [nodes[n]['flow'] for n in names], len(names)

def upper_limit(next, remaining, timeleft):
    i = 0
    val = flow[next]*timeleft
    # assume all nodes are reachable in 1 step (all caves inter-connected)
    for node in [n for n in remaining if n != next]:
        i += 1
        newtimeleft = timeleft - 2*i
        if newtimeleft > 0:
            val += flow[node]*newtimeleft
    return val

def next_move(node, timeleft, open=(), val=0):
    global best
    if val > best: # store the best score
        best = val
    # branch out greedily in order of descending valve flow
    next = tuple(i for i in range(nnodes) if i != node and i not in open and flow[i] > 0 and dist[node][i] + 2 < timeleft)
    for n in next:
        newtimeleft = timeleft - (dist[node][n] + 1)
        # estimate the upper limit of this path and skip the branch if futile
        if val + upper_limit(n, next, newtimeleft) <= best:
            continue
        next_move(n, newtimeleft, open + (n, ), val + flow[n]*newtimeleft)

def upper_limit2(node, transit, remaining, timeleft):
    # ignore transit for now
    val = 0
    val += flow[node[0]]*timeleft
    val += flow[node[1]]*timeleft
    # assume all nodes are reachable in 1 step
    next = [n for n in remaining if n not in node]
    i = 0
    for j in range(0, len(next) // 2):
        i += 1
        newtimeleft = timeleft - 2*i
        if newtimeleft > 0:
            val += flow[next[2*j]]*newtimeleft
            val += flow[next[2*j + 1]]*newtimeleft
    if len(next) % 2 == 1:
        i += 1
        newtimeleft = timeleft - 2*i
        if newtimeleft > 0:
            val += flow[next[-1]]*newtimeleft
    return val

def next_move2(node, timeleft, transit=(0, 0), open=(), val=0):
    global best2
    if val >= best2: # store the best score
        best2 = val
        #print("Max: {}, Val: {}, Path: {}".format(best2, val, [label[open[i]] for i in range(len(open))]))
    # branch out greedily in order of descending valve flow
    # both actors can move
    if transit[0] == 0 and transit[1] == 0:
        if node[0] == node[1]: # at beginning split the exploration to prevent exploring the search space twice
            next1 = tuple(i for i in range(0, nnodes, 2) if flow[i] > 0)
            next2 = tuple(i for i in range(1, nnodes, 2) if flow[i] > 0)
        else:
            next1 = tuple(i for i in range(nnodes) if i not in node and i not in open and flow[i] > 0 and dist[node[0]][i] + 2 < timeleft)
            next2 = tuple(i for i in range(nnodes) if i not in node and i not in open and flow[i] > 0 and dist[node[1]][i] + 2 < timeleft)
        for n1 in next1:
            d1 = dist[node[0]][n1] + 1
            for n2 in [n for n in next2 if n != n1]:
                d2 = dist[node[1]][n2] + 1
                # calculate the time till next event
                dmin = min(d1, d2)
                newtimeleft = timeleft - dmin
                # estimate the upper limit of this path and skip the branch if futile
                if val + upper_limit2((n1, n2), (0, 0), tuple(set(next1) | set(next2)), newtimeleft) <= best2:
                    return
                newopen = open
                newval = val
                if d1 - dmin == 0:
                    newopen += (n1,)
                    newval += flow[n1]*newtimeleft
                if d2 - dmin == 0:
                    newopen += (n2,)
                    newval += flow[n2]*newtimeleft
                next_move2((n1, n2), newtimeleft, (d1 - dmin, d2 - dmin), newopen, newval)
    # only actor 1 can move
    elif transit[0] == 0:
        next = tuple(i for i in range(nnodes) if i not in node and i not in open and flow[i] > 0 and dist[node[0]][i] + 2 < timeleft)
        # no more nodes to visit, actor 2 still in transit
        if len(next) == 0:
            newtimeleft = timeleft - transit[1]
            # estimate the upper limit of this path and skip the branch if futile
            if val + upper_limit2(node, (0, 0), next, newtimeleft) < best2:
                return
            next_move2(node, newtimeleft, (0, 0), open + (node[1],), val + flow[node[1]]*newtimeleft)
        for n in next:
            d1 = dist[node[0]][n] + 1
            # calculate the time till next event
            dmin = min(d1, transit[1])
            newtimeleft = timeleft - dmin
            # estimate the upper limit of this path and skip the branch if futile
            if val + upper_limit2(node, (0, 0), next, newtimeleft) < best2:
                continue
            newtransit = (d1 - dmin, transit[1] - dmin)
            newopen = open
            newval = val
            if d1 - dmin == 0:
                newopen += (n,)
                newval += flow[n]*newtimeleft
            if transit[1] - dmin == 0:
                newopen += (node[1],)
                newval += flow[node[1]]*newtimeleft
            next_move2((n, node[1]), newtimeleft, newtransit, newopen, newval)
    # only actor 2 can move
    elif transit[1] == 0:
        next = tuple(i for i in range(nnodes) if i not in node and i not in open and flow[i] > 0 and dist[node[1]][i] + 2 < timeleft)
        # no more nodes to visit, actor 1 still in transit
        if len(next) == 0:
            newtimeleft = timeleft - transit[0]
            # estimate the upper limit of this path and skip the branch if futile
            if val + upper_limit2(node, (0, 0), next, newtimeleft) < best2:
                return
            next_move2(node, newtimeleft, (0, 0), open + (node[0],), val + flow[node[0]]*newtimeleft)
        for n in next:
            d2 = dist[node[1]][n] + 1
            # calculate the time till next event
            dmin = min(d2, transit[0])
            newtimeleft = timeleft - dmin
            # estimate the upper limit of this path and skip the branch if futile
            if val + upper_limit2(node, (0, 0), next, newtimeleft) < best2:
                continue
            newtransit = (transit[0] - dmin, d2 - dmin)
            newopen = open
            newval = val
            if transit[0] - dmin == 0:
                newopen += (node[0], )
                newval += flow[node[0]]*newtimeleft
            if d2 - dmin == 0:
                newopen += (n, )
                newval += flow[n]*newtimeleft
            next_move2((node[0], n), newtimeleft, newtransit, newopen, newval)

dist, label, flow, nnodes = setup('input.txt')

best = 0
next_move(label.index('AA'), timeleft=30)
print("Part 1: {}".format(best))

best2 = 0
next_move2((label.index('AA'), label.index('AA')), timeleft=26)
print("Part 2: {}".format(best2))
