import numpy


class MinTreeGenerator(object):
    def __init__(self, algorithm='Prim'):
        super(MinTreeGenerator, self).__init__()
        self.generator = algorithm

    @staticmethod
    def kruskal(graph):
        return graph

    @staticmethod
    def prim(graph):
        return graph

    def build_tree(self, graph):
        if self.generator == 'Kruskal':
            return self.kruskal(graph)
        else:
            return self.prim(graph)


if __name__ == "__main__":
    G = [[]]
    myTreeGen = MinTreeGenerator('Prim')
    min_tree = myTreeGen.build_tree(G)
