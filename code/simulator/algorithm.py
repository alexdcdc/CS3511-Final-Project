D = {}
froms = {}
edges = {}

def clockwise(i, k, weights):
    n = len(weights)
    return (i + k + n) % n

def initialize_bridges(bridges, weights):
    for i in range(len(weights)):
        min_weight_index = clockwise(i, 1, weights)
        min_weight = weights[min_weight_index]
        j = clockwise(i, 2, weights)
        while j != i and min_weight > weights[i]:
            if weights[j] < min_weight:
                bridges[i][j] = min_weight_index
                min_weight = weights[j]
                min_weight_index = j
            j = clockwise(j, 1, weights)

def solve(weights, bridges, u, v, w):
    if (u, v, w) in D:
        return D[(u, v, w)]

    if v == clockwise(u, 1, weights):
        if w == -1:
            D[(u, v, w)] = 0
        else:
            D[(u, v, w)] = weights[u] * weights[v] * weights[w]
        return D[(u, v, w)]

    if w == -1: #v directly clockwise to u,
        v3 = bridges[u][v]
        if weights[u] < weights[v]:
            t1 = solve(weights, bridges, u, v3, -1)
            t2 = solve(weights, bridges, v3, v, u)
            froms[(u, v, w)] = [(u, v3, -1), (v3, v, u)]
            edges[(u, v, w)] = (v3, u)
        else:
            t1 = solve(weights, bridges, u, v3, v)
            t2 = solve(weights, bridges, v3, v, -1)
            froms[(u, v, w)] = [(u, v3, v), (v3, v, -1)]
            edges[(u, v, w)] = (v3, v)
        D[(u, v, w)] = t1 + t2
        return D[(u, v, w)]

    else:
        v4 = bridges[u][v]
        t1 = solve(weights, bridges, u, v, -1)
        t2 = solve(weights, bridges, u, v4, w)
        t3 = solve(weights, bridges, v4, v, w)

        branch1 = t1 + weights[u] * weights[v] * weights[w]
        branch2 = t2 + t3
        if (branch1 < branch2):
            froms[(u, v, w)] = [(u, v, -1)]
            edges[(u, v, w)] = (u, v)
        else:
            froms[(u, v, w)] = [(u, v4, w), (v4, v, w)]
            edges[(u, v, w)] = (w, v4)

        D[(u, v, w)] = min(t1 + weights[u] * weights[v] * weights[w], t2 + t3)
        return D[(u, v, w)]

def get_edge_list(k):
    if k not in edges:
        return []
    children = froms[k]
    l = [(k, edges[k])]

    for c in children:
        l = l + get_edge_list(c)

    return l


def solve_full(weights):
    n = len(weights)
    bridges = [[-1] * n for _ in range(n)]
    initialize_bridges(bridges, weights)
    v1 = weights.index(min(weights))
    v2 = weights.index(min([w for w in weights if w != weights[v1]]))
    # get indices of smallest and second smallest vertices
    result = solve(weights, bridges, v1, v2, -1) + solve(weights, bridges, v2, v1, -1)
    visited = [((-1, -1, -1), (v1, v2))] + get_edge_list((v1, v2, -1)) + get_edge_list((v2, v1, -1))
    visited = list(filter(lambda x: 1 < abs(x[1][0] - x[1][1]) < n - 1, visited))
    cones = [a[0] for a in visited]
    internal_edges = [a[1] for a in visited]
    print(cones, internal_edges)
    return result, internal_edges, cones

if __name__ == '__main__':
    print("Minimum triangulation is:", solve_full([4, 6, 10, 5]))
    # print("Minimum triangulation is:", solve_full([6, 10, 2, 1, 4, 3, 15, 5]))

