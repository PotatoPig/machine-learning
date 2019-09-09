def DT_classify(data, features, tree):
    root = next(iter(tree))
    subtree = tree[root]
    label_tag = features.index(root)
    for key in subtree.keys():
        if data[label_tag] == key:
            if type(subtree[key]).__name__ == 'dict':
                data_label = DT_classify(data, features, subtree[key])
            else:
                data_label = subtree[key]
    return data_label


def DT_accuracy(valdata, valfeatures, tree):
    total_data = len(valdata)
    right_class = 0
    for case in valdata:
        case_label = DT_classify(case, valfeatures, tree)
        if case_label == case[-1]:
            right_class += 1
    accuracy = right_class / total_data
    return accuracy
