# Dijkstra's algorithm adapted from: https://www.educative.io/answers/how-to-implement-dijkstras-algorithm-in-python
def dijkstra(edges, start):
    n = len(edges)
    visited = [[0, 0] if i == start else [0, 10000] for i in range(n)]
    def to_be_visited():
        v = -1
        for i in range(n):
            if visited[i][0] == 0 and (v < 0 or visited[i][1] <= visited[v][1]):
                v = i
        return v
    for i in range(n):
        v = to_be_visited()
        for j in range(n):
            if edges[v].get(j) and visited[j][0] == 0:
                dist = visited[v][1] + edges[v][j]
                if visited[j][1] > dist:
                    visited[j][1] = dist
        visited[v][0] = 1
    return(visited)

with open('input.txt') as file:
    lines = [line.rstrip() for line in file]
    hills = [list(map(lambda x: 0 if x == 'S' else 25 if x == 'E' else ord(x) - ord('a'), line)) for line in lines]
    nrow, ncol = len(lines), len(lines[0])
    graph = {i: {} for i in range(nrow*ncol)}
    start, end, startpos = None, None, []
    for i in range(nrow):
        for j in range(ncol):
            if (i == 0 or i == nrow - 1 or j == 0 or j == ncol - 1) and hills[i][j] == 0:
                startpos.append(ncol*i + j)
            if lines[i][j] == 'S':
                start = ncol*i + j
            elif lines[i][j] == 'E':
                end = ncol*i + j
            if j > 0 and hills[i][j] + 1 >= hills[i][j - 1]:
                graph[ncol*i + j][ncol*i + j - 1] = 1
            if j < ncol - 1 and hills[i][j] + 1 >= hills[i][j + 1]:
                graph[ncol*i + j][ncol*i + j + 1] = 1
            if i > 0 and hills[i][j] + 1 >= hills[i - 1][j]:
                graph[ncol*i + j][ncol*(i - 1) + j] = 1
            if i < nrow - 1 and hills[i][j] + 1 >= hills[i + 1][j]:
                graph[ncol*i + j][ncol*(i + 1) + j] = 1

distances = dijkstra(graph, start)
print("Part 1: {}".format(distances[end][1]))

# I prefer brute force, but it's faster to start from E using the transposed graph
graph2 = {i: {} for i in range(len(graph))}
for n1 in graph:
    for n2 in graph[n1]:
        graph2[n2][n1] = 1
distances = dijkstra(graph2, end)
res2 = []
for start in startpos:
    res2.append(distances[start][1])
print("Part 2: {}".format(min(res2)))
