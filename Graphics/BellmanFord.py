G = [[0, 6, float('inf'), 7, float('inf')],
     [float('inf'), 0, 5, 8, -4],
     [float('inf'), -2, 0, float('inf'), float('inf')],
     [float('inf'), float('inf'), -3, 0, 9],
     [2, float('inf'), 7, float('inf'), 0]]

# Choose the single source
source = 0


# Bellman Ford start
def bellman_ford(graph, source):
    m = len(graph)

    res = [float('inf') for i in range(m)]
    res[source] = 0

    for loop in range(len(res)-1):
        for i in range(m):
            for j in range(m):
                # Release every edge in the graph
                if graph[i][j] is not float('inf'):
                    if res[j] > res[i] + graph[i][j]:
                        res[j] = res[i] + graph[i][j]

    # Check if there is a negative loop in the graph
    for i in range(m):
        for j in range(m):
            # Release every edge in the graph
            if graph[i][j] is not float('inf'):
                if res[j] > res[i] + graph[i][j]:
                    return False

    return res


if __name__ == '__main__':
    result = bellman_ford(G, source)
    print(result)
