G = [[0, 3, 8, float('inf'), -4],
     [float('inf'), 0, float('inf'), 1, 7],
     [float('inf'), 4, 0, float('inf'), float('inf')],
     [2, float('inf'), -5, 0, float('inf')],
     [float('inf'), float('inf'), float('inf'), 6, 0]]


def floyd_warshall(graph):
    n = len(graph)
    D_old = graph
    for k in range(n):
        D_new = D_old.copy()
        for i in range(n):
            for j in range(n):
                D_new[i][j] = min(D_old[i][j], D_old[i][k] + D_old[k][j])
        D_old = D_new.copy()
    return D_new


if __name__ == '__main__':
    print(floyd_warshall(G))
