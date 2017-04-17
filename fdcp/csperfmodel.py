import pandas as pd
from sklearn.tree import DecisionTreeRegressor, export_graphviz
from graphviz import Source
from sklearn.externals import joblib
import sys
import logging
from terminaltables import AsciiTable


def prepare_data(training_data_file):
    raw_data = pd.read_csv(training_data_file)
    raw_data['block_size'] = raw_data['block_size'].apply(lambda bs: int(bs[:3]))
    return raw_data[['block_size', 'leaders', 'followers', 'write_pct']].copy().as_matrix(), raw_data[
        'iops'].copy().as_matrix()


def main(training_data_file, model_output, max_depth, test_data_file):
    regressor = DecisionTreeRegressor(max_depth=max_depth)
    x, y = prepare_data(training_data_file)
    regressor.fit(x, y)

    regr_tree_dot = export_graphviz(regressor, out_file=None,
                                    feature_names=['block_size', 'leaders', 'followers', 'write_pct'])
    regr_tree_src = Source(regr_tree_dot)
    regr_tree_src.render(model_output)
    joblib.dump(regressor, model_output + '.pkl')

    persisted_regressor = joblib.load(model_output + '.pkl')

    if test_data_file is not None:
        test_data_x, test_data_y = prepare_data(test_data_file)
        r = [['independent vars', 'prediction', 'actual', 'error']]
        for idx, t in enumerate(test_data_x):
            predicted_iops = persisted_regressor.predict(t.reshape(1, -1))
            error = test_data_y[idx] - predicted_iops[0]
            r.append([t, predicted_iops[0], test_data_y[idx], float(error) / test_data_y[idx]])

        print AsciiTable(r).table


# TODO:
#  - Logistic regression vs decision tree regression
#  - Utilizing the model in capacity planner
#

if __name__ == "__main__":
    if len(sys.argv) < 3:
        logging.error("""Missing arguments. \n\nUsage: python csperfmodel.py <training> <model output> [max-depth] [test]
                      """)
        exit(-1)

    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 5,
         sys.argv[4] if len(sys.argv) > 4 else None)
