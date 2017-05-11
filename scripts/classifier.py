import argparse
import collections
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score
from tripletools import get_best_features
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


plt.style.use('ggplot')

experiments = [
    {
        'name': 'Logistic Regression',
        'model': LogisticRegression(),
        'params': [
            {
                'solver': ['liblinear'],
                'penalty': ['l2'],
                'random_state': [77]
            },
        ]
    },
    {
        'name': 'SVM',
        'model': SVC(),
        'params': [
            {
                'kernel': ['poly'],
                'degree': [5],
                'random_state': [77]
            },
        ]
    },
    {
        'name': 'MLP',
        'model': MLPClassifier(max_iter=1000),
        'params': [
            {
                'hidden_layer_sizes': [(20, 10)],
                'random_state': [77]
            }
        ]
    },
    {
        'name': 'Random Forest',
        'model': RandomForestClassifier(),
        'params': [
            {
                'max_depth': [8],
                'n_estimators': [20],
                'min_samples_split': [5],
                'criterion': ['gini'],
                'max_features': ['auto'],
                'class_weight': ['balanced'],
                'random_state': [77]
            }
        ]
    },
]


def cross_validate_precision_recall_fbeta(model, X, y, cv=None):
    precision = cross_val_score(model, X, y, cv=cv, scoring='precision').mean()
    recall = cross_val_score(model, X, y, cv=cv, scoring='recall').mean()
    fbeta = cross_val_score(model, X, y, cv=cv, scoring='f1').mean()
    return precision, recall, fbeta


def plot_model_performance_comparison(experiments):
    fig, ax = plt.subplots()

    # Example data
    x_data = []
    y_dict = {
        'precision': {'color': '#f9f1c5', 'data': []},
        'recall': {'color': 'lightblue', 'data': []},
        'f1': {'color': 'green', 'data': []},
    }
    for exp in experiments:
        x_data.append(exp['name'])
        y_dict['precision']['data'].append(exp['best_score']['precision'])
        y_dict['recall']['data'].append(exp['best_score']['recall'])
        y_dict['f1']['data'].append(exp['best_score']['f1'])

    x = np.arange(len(x_data))
    width = 0.20
    i = 1
    legend_handles = []
    for label, y in y_dict.items():
        ax.bar(x + width * i, y['data'], width, color=y['color'])
        legend_handles.append(mpatches.Patch(color=y['color'], label=label))
        i += 1
    ax.set_xticks(x + width * 2)
    ax.set_xticklabels(x_data)
    ax.set_yticks(np.arange(0.0, 1.1, 0.1))
    ax.set_title('Triple Selector Models Performance')

    lgd = plt.legend(handles=legend_handles)
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train triples classifier')
    parser.add_argument('dataset_path', help='Dataset path')
    parser.add_argument('-o', '--output_path', help='Output model path', default='triples-classifier-model.pkl')
    parser.add_argument('-s', '--scaler_output_path', help='Output scaler path', default='triples-classifier-scaler.pkl')
    parser.add_argument('-b', '--best', help='search parameters that gives best model', action='store_true')
    args = parser.parse_args()

    # load dataset
    dataset = np.genfromtxt(args.dataset_path, delimiter=',', dtype='float32')
    total_features = dataset.shape[1] - 1

    # feature selection
    selected_features = get_best_features()
    print('Total features: {}'.format(total_features))
    print('Selected features: {} ({})'.format(selected_features, len(selected_features)))

    X = dataset[:, selected_features]
    y = dataset[:, -1]
    scaler = StandardScaler().fit(X)
    X = scaler.transform(X)
    joblib.dump(scaler, args.scaler_output_path)

    # collect dataset statistics
    counter = collections.Counter(y)
    print(counter)
    pos = counter[1] * 1.0 / (counter[0] + counter[1])
    neg = 1.0 - pos

    # exhaustive best parameters search
    cv = None
    print('')
    if args.best:
        best_score = 0.0
        best_model = None
        count = 0
        for experiment in experiments:
            search = GridSearchCV(
                estimator=experiment['model'],
                param_grid=experiment['params'],
                scoring='f1',
                cv=cv
            )
            search.fit(X, y)
            precision, recall, fbeta = cross_validate_precision_recall_fbeta(search.best_estimator_, X, y)
            print(search.best_estimator_)
            print('Precision: {}\nRecall: {}\nF1: {}\n'.format(
                precision,
                recall,
                fbeta
            ))
            experiment['best_model'] = best_model
            experiment['best_score'] = {'precision': precision, 'recall': recall, 'f1': fbeta}
            # replace current best model if the score is higher
            if search.best_score_ > best_score:
                best_score = search.best_score_
                best_model = search.best_estimator_
            count += 1
        print('--------------- Result ----------------')
        print('Best models: {} (F1 = {})'.format(best_score, type(best_model).__name__))
        model = best_model

        # show plot
        plot_model_performance_comparison(experiments)

    else:
        model = RandomForestClassifier(max_depth=8, class_weight='balanced', n_estimators=20, min_samples_leaf=1)

        # cross validate best model to compare score
        precision, recall, fbeta = cross_validate_precision_recall_fbeta(model, X, y)
        print('Precision: {}'.format(precision))
        print('Recall: {}'.format(recall))
        print('F1-Score: {}'.format(fbeta))

    # save model to file
    joblib.dump(model, args.output_path)
    print('Model saved to {}'.format(args.output_path))
    print('Scaler saved to {}'.format(args.scaler_output_path))
