weights = [1, 4, 3, 6, 10, 2]
n = len(weights)
# bridges[i][j] stores:
#   the next smallest weight + corresponding index between i,j if (i,j) is a bridge, OR
#   -1 if (i,j) is not a bridge

bridges = [[(-1, -1)] * n for _ in range(n)]



def print_2d(arr):
    print('\n'.join(['\t'.join(map(str, row)) for row in arr]))

def clockwise(i, k):
    return (i + k + n) % n

def is_adjacent(i, j):
    return j == clockwise(i, 1) or j == clockwise(i, -1)

def precedes(i, j, k):
    j_dist = (j - i + n) % n
    k_dist = (k - i + n) % n
    if j_dist < k_dist:
        return j, k
    return k, j


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
# NOTE: ASSUME weights[u] < weights[v]
# 3 cases:
    # one adjacent
    # both adjacent
    # netiher adjacent
def solve(u, v, w):
    if (u, v, w) in D:
        return D[(u, v, w)]

    v1, v2, v3 = (w, u, v) if w != 0 else (u, v, bridges[u][v])
    x, y = precedes(v1, v2, v3)
    result = 0
    
    if is_adjacent(v1, v2) and is_adjacent(v1, v3):
        v4 = bridges[x][y]
        branch_one = v1 * v2 * v3 + solve(x, y, 0)
        branch_two = solve(x, v4, v1) + solve(v4, y, v1)

        result = min(branch_one, branch_two)

    elif not is_adjacent(v1, v2) and not is_adjacent(v1, v3):
        result = solve(v1, x, 0) + solve(x, y, v1) + solve(y, v1, 0)

    else:
        a, b = (v2, v3) if is_adjacent(v1, v2) else (v3, v2)
        if (a == x):
            result = solve(x, y, v1) + solve(y, v1, 0)
        else:
            result = solve(v1, x, 0) + solve(x, y, v1)

    D[(u, v, w)] = result
    return result

if __name__ == '__main__':
    # Assume all vertex weights are distinct
    initialize_bridges()
    print_2d(bridges)
