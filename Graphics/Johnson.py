from BellmanFord import bellman_ford
from Dijkstra import dijkstra
import copy

G = [[0, 3, 8, float('inf'), -4],
     [float('inf'), 0, float('inf'), 1, 7],
     [float('inf'), 4, 0, float('inf'), float('inf')],
     [2, float('inf'), -5, 0, float('inf')],
     [float('inf'), float('inf'), float('inf'), 6, 0]]

def johnson(graph):
    result = []

    n = len(graph)

    source = 0
    new_graph = copy.deepcopy(graph)
    for edge in range(n):
        new_graph[source][edge] = min(0, new_graph[source][edge])

    node_weight = bellman_ford(graph=new_graph, source=source)
    print(node_weight)
    # graph weight change
    print(graph)
    for i in range(n):
        for j in range(n):
            graph[i][j] = graph[i][j] + node_weight[i] - node_weight[j]
    print(graph)

    for k in range(n):
        out = dijkstra(graph=graph, source=k)
        result.append(out)

    return result


if __name__ == '__main__':
    test = johnson(G)
    print(test)
