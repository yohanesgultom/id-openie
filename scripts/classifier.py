"""
classifier.py
@author yohanes.gultom@ui.ac.id

Running experiments:
* Comparing triple classifiers (optimized by grid search) performance using cross validation
* Comparing feature sets performance agains the best triple classifier

Train models:
* Train triple classifier model using the best model and feature set then save it to binary file

"""

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
from sklearn.model_selection import cross_val_score, cross_validate
from sklearn.metrics import precision_recall_fscore_support, recall_score, precision_score, f1_score, make_scorer
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
                'activation': ['relu'],
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

feature_sets = [
    {
        'name': '1',
        'desc': 'Current POS tag + Head POS tag',
        'features': [0, 2, 10, 12, 17, 19]
    },
    {
        'name': '2',
        'desc': 'Current POS tag + Head POS tag + DepRel',
        'features': [0, 1, 2, 10, 11, 12, 17, 18, 19]
    },
    {
        'name': '3',
        'desc': 'Current POS tag + Head POS tag + DepRel + Named-Entity',
        'features': [0, 1, 2, 3, 10, 11, 12, 13, 17, 18, 19, 20]
    },
    {
        'name': '4',
        'desc': 'Current POS tag + Head POS tag + DepRel + Named-Entity + Distance from Predicate',
        'features': [0, 1, 2, 3, 5, 10, 11, 12, 13, 17, 18, 19, 20, 22]
    },
    {
        'name': '5',
        'desc': 'Current POS tag + Head POS tag + DepRel + Named-Entity + Distance from Predicate + Dependents Count',
        'features': [0, 1, 2, 3, 4, 5, 10, 11, 12, 13, 14, 17, 18, 19, 20, 21, 22]
    },
    {
        'name': '6',
        'desc': 'Current POS tag + Head POS tag + DepRel + Distance from Predicate + Dependents Count + Dependency with Predicate',
        'features': [0, 1, 2, 4, 5, 6, 10, 11, 12, 14, 17, 18, 19, 21, 22, 23]
    },
    {
        'name': '7',
        'desc': 'Current POS tag + Head POS tag + DepRel + Subject and Object Named-Entities + Distance from Predicate + Dependents Count Predicate and Object + Dependency with Predicate',
        'features': [0, 1, 2, 3, 5, 6, 10, 11, 12, 14, 17, 18, 19, 20, 21, 22, 23]
    },
    {
        'name': 'All',
        'desc': 'Current POS tag + Head POS tag + DepRel + Named-Entity + Distance from Predicate + Dependents Count + Neighbouring POS tags + Dependency with Predicate',
        'features': range(27)
    }
]


def extract_features(dataset, selected_features):
    total_features = dataset.shape[1] - 1

    print('Total features: {}'.format(total_features))
    print('Selected features: {} ({})'.format(selected_features, len(selected_features)))

    X = dataset[:, selected_features]
    y = dataset[:, -1]
    scaler = StandardScaler().fit(X)
    X = scaler.transform(X)

    # collect dataset statistics
    counter = collections.Counter(y)
    print(counter)
    pos = counter[1] * 1.0 / (counter[0] + counter[1])
    neg = 1.0 - pos
    return X, y, scaler


def plot_comparison_chart(experiments, title, cv, score_field='best_score'):
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
        y_dict['precision']['data'].append(exp[score_field]['precision'])
        y_dict['recall']['data'].append(exp[score_field]['recall'])
        y_dict['f1']['data'].append(exp[score_field]['f1'])

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
    ax.set_title('{} \n k-fold cross-validation k={}'.format(title, cv))

    lgd = plt.legend(handles=legend_handles)
    plt.show()


def print_comparison_table(experiments, score_field='best_score'):
    print('Model\tPrecision\tRecall\tF1')
    for exp in experiments:
        print('{}\t{}\t{}\t{}'.format(
            exp['name'],
            exp[score_field]['precision'],
            exp[score_field]['recall'],
            exp[score_field]['f1']
        ))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train triples classifier')
    parser.add_argument('dataset_path', help='Dataset path')
    parser.add_argument('-o', '--output_path', help='Output model path', default='triples-classifier-model.pkl')
    parser.add_argument('-s', '--scaler_output_path', help='Output scaler path', default='triples-classifier-scaler.pkl')
    parser.add_argument('-m', '--mode', help='select mode', choices=['compare_models', 'compare_features', 'train_model'], default='train_model')
    parser.add_argument('--nocv', help='no cross-validation. training accuracy only', action='store_true')
    parser.add_argument('--cv', help='value of k for k-fold cross-validation', type=int, default=3)
    args = parser.parse_args()

    # load dataset
    dataset = np.genfromtxt(args.dataset_path, delimiter=',', dtype='float32')

    # exhaustive best parameters search
    cv = args.cv
    print('cv = {}\n'.format(cv))
    if args.mode == 'compare_models':
        best_score = 0.0
        best_model = None

        # feature selection
        X, y, scaler = extract_features(dataset, get_best_features())
        joblib.dump(scaler, args.scaler_output_path)

        for experiment in experiments:
            search = GridSearchCV(
                estimator=experiment['model'],
                param_grid=experiment['params'],
                scoring='f1',
                cv=cv
            )
            search.fit(X, y)
            if args.nocv:
                y_pred = search.best_estimator_.predict(X)
                precision, recall, fbeta, support = precision_recall_fscore_support(y, y_pred, average='binary')
                fbeta_min = fbeta_max = fbeta_std = fbeta
            else:
                cv_results = cross_validate(search.best_estimator_, X, y=y, scoring=['precision', 'recall'], cv=cv)
                recall = cv_results['test_recall'].mean()
                precision = cv_results['test_precision'].mean()
                fbeta = 2 * recall * precision / (recall + precision)

            experiment['best_score'] = {'precision': precision, 'recall': recall, 'f1': fbeta}
            # replace current best model if the score is higher
            if search.best_score_ > best_score:
                best_score = search.best_score_
                best_model = search.best_estimator_

        print('--------------- Result ----------------')
        print('Best models: {} (F1 = {})'.format(best_score, type(best_model).__name__))
        print(best_model)

        # print table
        print('--------------- Table ----------------')
        print_comparison_table(experiments, score_field='best_score')

        # show plot
        plot_comparison_chart(experiments, 'Triple Selector Models Performance', cv, score_field='best_score')

    elif args.mode == 'compare_features':
        # best score and feature set var
        best_score = 0
        best_model = None
        best_set = None

        # best hyperparameters for the best model
        best_params = experiments[3]['params'][0]
        for feature_set in feature_sets:
            X, y, scaler = extract_features(dataset, feature_set['features'])

            # only use the best model
            model = RandomForestClassifier(
                max_depth=best_params['max_depth'][0],
                class_weight=best_params['class_weight'][0],
                n_estimators=best_params['n_estimators'][0],
                min_samples_split=best_params['min_samples_split'][0],
                max_features=best_params['max_features'][0],
                random_state=best_params['random_state'][0]
            )

            # cross_validate
            cv_results = cross_validate(model, X, y=y, scoring=['precision', 'recall'], cv=cv)
            recall = cv_results['test_recall'].mean()
            precision = cv_results['test_precision'].mean()
            fbeta = 2 * recall * precision / (recall + precision)
            feature_set['cv_score'] = {'precision': precision, 'recall': recall, 'f1': fbeta}

            if best_score < fbeta:
                best_score = fbeta
                best_set = feature_set

        # print result
        print('--------------- Result ----------------')
        print('Best feature set: {} (F1 = {})'.format(best_score, best_set))

        # print table
        print('--------------- Table ----------------')
        print_comparison_table(feature_sets, score_field='cv_score')

        # show plot
        plot_comparison_chart(feature_sets, 'Triple Selector Feature Sets Performance', cv, score_field='cv_score')

        print('\nInformation:')
        for feature_set in feature_sets:
            print('{}\t{}\t{}'.format(feature_set['name'], feature_set['desc'], feature_set['features']))

    else:  # if args.mode == 'train_model'

        # feature selection
        X, y, scaler = extract_features(dataset, get_best_features())
        joblib.dump(scaler, args.scaler_output_path)

        best_params = experiments[3]['params'][0]
        model = RandomForestClassifier(
            max_depth=best_params['max_depth'][0],
            class_weight=best_params['class_weight'][0],
            n_estimators=best_params['n_estimators'][0],
            min_samples_split=best_params['min_samples_split'][0],
            max_features=best_params['max_features'][0],
            random_state=best_params['random_state'][0]
        )

        # train and test using trainig data
        model.fit(X, y)
        y_pred = model.predict(X)
        precision, recall, fbeta, support = precision_recall_fscore_support(y, y_pred, average='binary')
        fbeta_min = fbeta_max = fbeta_std = fbeta

        # save model to file
        if model:
            joblib.dump(model, args.output_path)
            print('Model saved to {}'.format(args.output_path))
            print('Scaler saved to {}'.format(args.scaler_output_path))
