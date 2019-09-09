class Node(object):
    def __init__(self, name=None, node_data=None, weight=None, tail=None):
        self._name = name
        self._node_data = node_data
        self._weight = weight
        self._tail = tail

    # change the value in this node
    def set_value(self, new_name):
        self._name = new_name

    def set_node_data(self, new_node_data):
        self._node_data = new_node_data

    def set_weight(self, new_weight):
        self._weight = new_weight

    def set_tail(self, new_tail):
        self._tail = new_tail

    # get the info of this node
    def get_value(self):
        return self._name

    def get_node_data(self,):
        return self._node_data

    def get_weight(self):
        return self._weight

    def get_next(self):
        return self._tail


class Graph(object):
    def __init__(self, adjasent_list=[]):
        self._vertex_list = adjasent_list

    def get_num_of_vertexs(self):
        return len(self._vertex_list)

    def add_vertex(self, new_vertex):
        self._vertex_list.append(new_vertex)