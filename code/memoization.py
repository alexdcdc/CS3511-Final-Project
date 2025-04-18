weights = [1, 2, 4, 3]
n = len(weights)

bridges = [[-1] * n for _ in range(n)]

def clockwise(i, k):
    return (i + k + n) % n

def initialize_bridges():
    for i in range(len(weights)):
        min_weight_index = clockwise(i, 1)
        min_weight = weights[min_weight_index]
        j = clockwise(i, 2)
        while j != i and min_weight > weights[i]:
            if weights[j] < min_weight:
                bridges[i][j] = min_weight_index
                min_weight = weights[j]
                min_weight_index = j

            j = clockwise(j, 1)

D = {}
def solve(u, v, w):
    if (u, v, w) in D:
        return D[(u, v, w)]

    if v == clockwise(u, 1):
        if w == -1:
            D[(u, v, w)] = 0
        else:
            D[(u, v, w)] = weights[u] * weights[v] * weights[w]
        return D[(u, v, w)]

    if w == -1: #v directly clockwise to u,
        v3 = bridges[u][v]
        if weights[u] < weights[v]:
            t1 = solve(u, v3, -1)
            t2 = solve(v3, v, u)
        else:
            t1 = solve(u, v3, v)
            t2 = solve(v3, v, -1)
        D[(u, v, w)] = t1 + t2
        return D[(u, v, w)]

    else:
        v4 = bridges[u][v]
        t1 = solve(u, v, -1)
        t2 = solve(u, v4, w)
        t3 = solve(v4, v, w)
        D[(u, v, w)] = min(t1 + weights[u] * weights[v] * weights[w], t2 + t3)
        return D[(u, v, w)]

def solve_full():
    initialize_bridges()
    v1 = weights.index(min(weights))
    v2 = weights.index(min([w for w in weights if w != weights[v1]]))
    # get indices of smallest and second smallest vertices

    return solve(v1, v2, -1) + solve(v2, v1, -1)

if __name__ == '__main__':
    print("Given vertices:", str(weights))
    print("Minimum triangulation is:", solve_full())
