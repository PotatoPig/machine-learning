from math import log


def get_information_entropy(dataset):

    total_data = len(dataset)
    data_types = {}

    for datavec in dataset:
        curlabel = datavec[-1]
        if curlabel not in data_types.keys():
            data_types[curlabel] = 0
        data_types[curlabel] += 1

    inf_entropy = 0
    for i in data_types:
        pi = data_types[i]/total_data
        inf_entropy -= pi*log(pi, 2)

    return inf_entropy


def get_gini(dataset):
    total_data = len(dataset)
    data_types = {}

    for data_vec in dataset:
        cur_label = data_vec[-1]
        if cur_label not in data_types.keys():
            data_types[cur_label] = 0
        data_types[cur_label] += 1

    gini_data = 1
    for k in data_types:
        pk = data_types[k] / total_data
        gini_data -= pk * pk

    return gini_data


# ID3 algorithm
def get_information_gain(data_set, features, features_dic, prop):
    prop_tag = features.index(prop)
    data_amount = len(data_set)

    prop_sort = {}
    for prop_value in features_dic[prop]:
        prop_box = [example for example in data_set if example[prop_tag] == prop_value]
        prop_sort[prop_value] = prop_box

    inf_gain = get_information_entropy(data_set)
    for item in prop_sort:
        item_amount = len(prop_sort[item])
        inf_gain -= item_amount/data_amount*get_information_entropy(prop_sort[item])

    return inf_gain


# C4.5 algorithm
def get_information_gain_ratio(data_set, features, features_dic, prop):
    prop_tag = features.index(prop)
    data_amount = len(data_set)

    prop_sort = {}
    for prop_value in features_dic[prop]:
        prop_box = [example for example in data_set if example[prop_tag] == prop_value]
        prop_sort[prop_value] = prop_box

    intrinsic_value = 0
    for item in prop_sort:
        item_amount = len(prop_sort[item])
        intrinsic_value -= item_amount/data_amount * log(item_amount/data_amount, 2)

    inf_gain = get_information_gain(data_set, features, features_dic, prop)
    inf_gain_ratio = inf_gain/intrinsic_value
    print(prop, intrinsic_value)

    return inf_gain_ratio


# CART algorithm
def get_gini_index(data_set, features, features_dic, prop):
    prop_tag = features.index(prop)
    data_amount = len(data_set)

    prop_sort = {}
    for prop_value in features_dic[prop]:
        prop_box = [example for example in data_set if example[prop_tag] == prop_value]
        prop_sort[prop_value] = prop_box

    gini_index = 0
    for item in prop_sort:
        item_amount = len(prop_sort[item])
        gini_index += item_amount / data_amount * get_gini(prop_sort[item])

    return gini_index


def split_branch(data_set, features, prop, prop_value):
    prop_tag = features.index(prop)
    branch = [example for example in data_set if example[prop_tag] == prop_value]
    # print(prop_value, branch, '\n')
    return branch


def choose_best_feature(data_set, features, features_dic, feature_set):

    feature_information_gain = {}
    for feature in feature_set:
        feature_information_gain[feature] = get_information_gain(data_set, features, features_dic, feature)
    # print(feature_information_gain)

    feature_key = list(feature_information_gain.keys())
    feature_value = list(feature_information_gain.values())
    best_value = max(feature_value)
    feature_tag = feature_value.index(best_value)
    bestfeature = feature_key[feature_tag]

    return bestfeature, best_value


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


def create_decision_tree(data_set, features, features_dic, feature_set):

    threshold = -100
    class_list = list(count_classes(data_set).keys())
    if len(class_list) == 1:
        return class_list[0]
    elif len(feature_set) == 0:
        return major_class(data_set)
    else:
        best_feature, best_inf_gain = choose_best_feature(data_set, features, features_dic, feature_set)
        if best_inf_gain <= threshold:
            return major_class(data_set)
        else:
            decision_tree = {best_feature: {}}
            feature_set.remove(best_feature)
            for feature_value in features_dic[best_feature]:
                branch_feature_set = feature_set
                branch_dataset = split_branch(data_set, features, best_feature, feature_value)
                if len(branch_dataset) == 0:
                    decision_tree[best_feature][feature_value] = major_class(data_set)
                else:
                    decision_tree[best_feature][feature_value] = create_decision_tree(branch_dataset,
                                                                                      features,
                                                                                      features_dic,
                                                                                      branch_feature_set)

    return decision_tree
