import pandas as pd
from sklearn.tree import DecisionTreeRegressor, export_graphviz
from graphviz import Source
from sklearn.externals import joblib
import sys
import logging


def prepare_training_data(training_data_file):
    raw_data = pd.read_csv(training_data_file)
    raw_data['block_size'] = raw_data['block_size'].apply(lambda bs: int(bs[:3]))
    return raw_data[['block_size', 'leaders', 'followers', 'write_pct']].copy().as_matrix(), raw_data[
        'iops'].copy().as_matrix()


def prepare_test_data(test_data_file):
    raw_data = pd.read_csv(test_data_file)
    raw_data['block_size'] = raw_data['block_size'].apply(lambda bs: int(bs[:3]))
    return raw_data[['block_size', 'leaders', 'followers', 'write_pct']].copy().as_matrix(), raw_data[
        'iops'].copy().as_matrix()


def main(training_data_file, model_output, max_depth, test_data_file):
    regressor = DecisionTreeRegressor(max_depth=max_depth)
    x, y = prepare_training_data(training_data_file)
    regressor.fit(x, y)
    regr_tree_dot = export_graphviz(regressor, out_file=None, feature_names=['block_size', 'leaders', 'followers', 'write_pct'])
    regr_tree_src = Source(regr_tree_dot)
    regr_tree_src.render(model_output)
    joblib.dump(regressor, model_output + '.pkl')


# TODO:
#  - Logistic regression vs decision tree regression
#  - Model persistence (Choose the simplest method since training takes small amount of time and retraining is possible)
#  - Utilizing the model in capacity planner
#
# Immediate tasks:
#  - Need separate training and test data sets
#  -

if __name__ == "__main__":
    if len(sys.argv) < 3:
        logging.error("""Missing arguments. \n\nUsage: python csperfmodel.py <training> <model output> [max-depth] [test]
                      """)
        exit(-1)

    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else None, sys.argv[4] if len(sys.argv) > 4 else 5)
