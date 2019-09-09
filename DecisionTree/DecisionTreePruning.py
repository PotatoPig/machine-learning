import copy
from WatermelonDataSet_2 import createDataSet
from DecisionTreeValidate import DT_accuracy
from DecisionTreeVisualization import tree_plot

test_tree = {'纹理': {'清晰': {'脐部': {'凹陷': '好瓜',
                                        '平坦': '坏瓜',
                                        '稍凹': {'色泽': {'青绿': '好瓜',
                                                          '浅白': '好瓜',
                                                          '乌黑': {'触感': {'硬滑': '好瓜',
                                                                            '软粘': '坏瓜'}}}}}},
                      '模糊': '坏瓜',
                      '稍糊': {'敲击': {'沉闷': '坏瓜',
                                        '清脆': '坏瓜',
                                        '浊响': {'根蒂': {'稍蜷': '好瓜',
                                                          '蜷缩': '好瓜',
                                                          '硬挺': '好瓜'}}}}}}


def tree_prune(tree, test_data, features):
    nodes = get_nodes(tree)
    prune_list = get_prune_list(nodes)
    while prune_list:
        pruning_node = prune_list.pop()
        if type(pruning_node).__name__ == 'set':
            '''
            before_prune = DT_accuracy(test_data, features, tree)
            majorlabel = major_class(test_data)
            count = 0
            for data in test_data:
                if data[-1] == majorlabel:
                    count += 1
            after_prune = count/len(test_data)
            if after_prune > before_prune:
                tree = {majorlabel}
            '''
            return tree
        elif type(pruning_node).__name__ == 'dict':
            node_data = get_node_data(pruning_node, test_data, features)
            classlabel = major_class(node_data)
            before_prune = DT_accuracy(test_data, features, tree)
            # tree_plot(tree)
            # print(before_prune)
            tree, originalleaf = prune(tree, pruning_node, classlabel)
            after_prune = DT_accuracy(test_data, features, tree)
            # tree_plot(tree)
            # print(after_prune)
            if after_prune <= before_prune:
                tree, label = prune(tree, pruning_node, originalleaf)

    return tree


def prune(tree, prunepath, label):
    subprune = prunepath
    root = next(iter(subprune))
    subtree = tree
    while type(subprune[root]).__name__ == 'dict':
        subprune = subprune[root]
        subtree = subtree[root]
        root = next(iter(subprune))
    leaf = subtree[root]
    subtree[root] = label
    return tree, leaf


def get_nodes(tree):
    nodes = []
    root = next(iter(tree))
    subtree = tree[root]
    store_branch = {root:{}}
    nodes.append({root})
    for key in subtree.keys():
        if type(subtree[key]).__name__ == 'dict':
            sub_nodes = get_nodes(subtree[key])
            for x in sub_nodes:
                store_branch[root] = {key: x}
                nodes.append(store_branch.copy())
    return nodes


def get_node_depth(node_path):
    if type(node_path).__name__ == 'set':
        return 1
    length = 1
    root = next(iter(node_path))
    sub_leaf = node_path[root]
    value = next(iter(sub_leaf))
    if type(sub_leaf).__name__ == 'dict':
        length += get_node_depth(sub_leaf[value])
        return length


def get_prune_list(nodes):
    prune_list = []
    length_set = set()
    for item in nodes:
        l = get_node_depth(item)
        if l not in length_set:
            length_set.add(l)
    length_list = list(length_set)
    length_list.sort(reverse=True)
    while length_list:
        top = length_list.pop()
        for item in nodes:
            if get_node_depth(item) == top:
                prune_list.append(item)
    return prune_list


def get_node_data(node_path, dataset, features):
    if type(node_path).__name__ == 'set':
        return dataset
    root = next(iter(node_path))
    sub_leaf = node_path[root]
    if type(sub_leaf).__name__ == 'dict':
        prop_tag = features.index(root)
        value = next(iter(sub_leaf))
        leaf_data = [example for example in dataset if example[prop_tag] == value]
        return get_node_data(node_path[root][value], leaf_data, features)


def major_class(data_set):
    class_count = count_classes(data_set)
    class_name = list(class_count.keys())
    class_number = list(class_count.values())
    major = class_name[class_number.index(max(class_number))]
    return major


def count_classes(data_set):
    class_count = {}
    for data_vec in data_set:
        cur_class = data_vec[-1]
        if cur_class not in class_count.keys():
            class_count[cur_class] = 0
        class_count[cur_class] += 1
    return class_count


if __name__ == "__main__":
    DataSet, Features, FeaturesDic = createDataSet()
    node_paths = get_nodes(test_tree)
    priority_list = get_prune_list(node_paths)
    for i in priority_list:
        print(i, get_node_depth(i))
        print('\n')
        # print(get_node_data(i, DataSet, Features))
    res, leaf = prune(test_tree, priority_list[len(priority_list) - 1], '好瓜')
    print(res, leaf)

