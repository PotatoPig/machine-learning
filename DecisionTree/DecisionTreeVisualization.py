# -*- coding: utf-8 -*-
from pylab import *
import matplotlib.pyplot as plt

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


decisionNode = dict(boxstyle="sawtooth", fc="1")
leafNode = dict(boxstyle="round4", fc="1")
arrow_args = dict(arrowstyle="<-")

# get the number of leaves, so we can decide the width of the figure
def get_tree_leafs(tree):
    leaf_num = 0
    root = next(iter(tree))
    subtree = tree[root]
    for branch in subtree.keys():
        if type(subtree[branch]).__name__ == 'dict':  # 如果模块是被导入，__name__的值为模块名字
            leaf_num += get_tree_leafs(subtree[branch])
        else:
            leaf_num += 1
    return leaf_num


# get the number of depth, so we can decide the height of the figure
def get_tree_depth(tree):
    depth = 0
    root = next(iter(tree))  # dict.keys() 返回字典的 keys
    subtree = tree[root]
    for branch in subtree.keys():
        if type(subtree[branch]).__name__ == 'dict':  # 如果模块是被导入，__name__的值为模块名字
            cur_depth = get_tree_depth(subtree[branch]) + 1
        else:
            cur_depth = 1
        if cur_depth > depth:
            depth = cur_depth
    return depth


def plot_node(text, end_pt, start_pt, node_type):
    arrow_args = dict(arrowstyle="<-")  # 定义箭头格式
    font = matplotlib.font_manager.FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=8)
    tree_plot.ax1.annotate(text, xy=start_pt, xycoords='axes fraction',
                                 xytext=end_pt, textcoords='axes fraction',
                                 va="center", ha="center", bbox=node_type,
                                 arrowprops=arrow_args, FontProperties=font)



def plot_branch_value(start_pt, end_pt, value):
    x_mid = (start_pt[0] - end_pt[0])/2.0 + end_pt[0]
    y_mid = (start_pt[1] - end_pt[1])/2.0 + end_pt[1]
    font = matplotlib.font_manager.FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=8)
    tree_plot.ax1.text(x_mid, y_mid, value, va="center", ha="center", rotation=0, FontProperties=font)


def plot_tree(tree, root_pt, text):
    decisionNode = dict(boxstyle="sawtooth", fc="0.8")  # 设置结点格式
    leafNode = dict(boxstyle="round4", fc="0.8")
    tree_leafs = get_tree_leafs(tree)
    tree_depth = get_tree_depth(tree)
    root = next(iter(tree))
    subtree = tree[root]
    center_pt = (plot_tree.xOff + (1.0 + float(tree_leafs)) / 2.0 / plot_tree.totalleaf, plot_tree.yOff)
    plot_branch_value(root_pt, center_pt, text)  # 画分支上的键
    plot_node(root, center_pt, root_pt, decisionNode)
    plot_tree.yOff = plot_tree.yOff - 1.0 / plot_tree.totaldepth
    for branch in subtree.keys():
        if type(subtree[branch]).__name__=='dict':
            plot_tree(subtree[branch], center_pt, branch)
        else:
            plot_tree.xOff = plot_tree.xOff + 1.0 / plot_tree.totalleaf
            plot_node(subtree[branch], (plot_tree.xOff, plot_tree.yOff), center_pt, leafNode)
            plot_branch_value((plot_tree.xOff, plot_tree.yOff), center_pt, str(branch))
    plot_tree.yOff = plot_tree.yOff + 1.0 / plot_tree.totaldepth


def tree_plot(tree):
    fig = plt.figure(1, figsize=(5, 3.8), dpi=150, facecolor='white')  # 创建fig
    fig.clf()  # 清空fig
    tree_plot.ax1 = plt.subplot(111, frameon=False)  # 去掉x、y轴
    plot_tree.totalleaf = float(get_tree_leafs(tree))  # 获取决策树叶结点数目
    plot_tree.totaldepth = float(get_tree_depth(tree))  # 获取决策树层数
    plot_tree.xOff = -0.5 / plot_tree.totalleaf
    plot_tree.yOff = 1.0  # x偏移
    plot_tree(tree, (0.5, 1.0), '')  # 绘制决策树
    plt.axis('off')
    plt.show()  # 显示绘制结果


if __name__ == '__main__':
    tree_plot(test_tree)


