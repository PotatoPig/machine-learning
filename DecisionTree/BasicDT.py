from WatermelonDataSet_2 import createDataSet
from WatermelonDataSet_2_v2 import createTrainDataSet, createValDataSet
from DecisionTreeGeneration import create_decision_tree
from DecisionTreeValidate import DT_accuracy
from DecisionTreeVisualization import tree_plot
from DecisionTreePruning import tree_prune


DataSet, Features, FeaturesDic = createTrainDataSet()
FeatureSet = set(Features)
res_tree = create_decision_tree(DataSet, Features, FeaturesDic, FeatureSet)
tree_plot(res_tree)

ValData, ValFeatures, ValFeaturesDic = createValDataSet()
accuracy = DT_accuracy(ValData, ValFeatures, res_tree)
print(accuracy)

res_tree = tree_prune(res_tree, ValData, ValFeatures)
tree_plot(res_tree)
accuracy = DT_accuracy(ValData, ValFeatures, res_tree)
print(accuracy)

