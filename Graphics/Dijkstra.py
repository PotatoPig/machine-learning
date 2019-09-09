G = [[0, 10, float('inf'), 5, float('inf')],
     [float('inf'), 0, 1, 2, float('inf')],
     [float('inf'), float('inf'), 0, float('inf'), 4],
     [float('inf'), 3, 9, 0, 2],
     [7, float('inf'), 6, float('inf'), 0]]

# Choose the single source
source = 0


# Bellman Ford start
def dijkstra(graph, source):
    m = len(graph)

    res = [float('inf')] * m
    res[source] = 0

    min_heap = {}
    for k in range(m):
        min_heap[k] = res[k]

    while len(min_heap) > 0:
        for key in min_heap.keys():
            min_heap[key] = res[key]

        node_list = list(min_heap.keys())
        value_list = list(min_heap.values())
        min_value = min(value_list)
        min_node = node_list[value_list.index(min_value)]

        for j in range(m):
            if graph[min_node][j] < 0:
                return False
            if graph[min_node][j] is not float('inf'):
                if res[j] > res[min_node] + graph[min_node][j]:
                    res[j] = res[min_node] + graph[min_node][j]
        min_heap.pop(min_node)

    return res


if __name__ == '__main__':
    result = dijkstra(G, source)
    print(result)