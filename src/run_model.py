"""
Optimize and fit an SVC model on training data. Scores it on the test data,
then produces scores and confusion matrices
Usage: run_model.py --model=<model> --in_dir=<in_dir> --out_dir=<out_dir> 
 
Options:
--model=<model>           Model to run (knn | svc | both)
--in_dir=<in_dir>         Path to processed data folder
--out_dir=<out_dir>       Path to folder in which to export the results

Arguments:
    model: knn - kNN model
           svc - SVC model
           both - runs both the kNN model and the SVC model
"""

# Imports
import os
import numpy as np
import pandas as pd
from scipy.stats import randint, loguniform
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.model_selection import cross_validate, RandomizedSearchCV, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import pickle
from docopt import docopt, DocoptExit


def get_data_splits(in_dir, train=True):
    if train:
        data_type = 'train.csv'
    else:
        data_type = 'test.csv'            
    df = pd.read_csv(os.path.join(in_dir, data_type))
    
    X, y = df.drop(columns=['TYPE1']), df['TYPE1']
    return X, y


def get_pipe_search(model, preprocessor):

    if model == 'knn':
        param_dist = {
        'kneighborsclassifier__n_neighbors': range(1, 20)
        }
        estimator = KNeighborsClassifier()
        search = GridSearchCV

    elif model == 'svc':
        param_dist = {
        "svc__gamma": loguniform(1e-2, 1e3),
        "svc__C": loguniform(1e-2, 1e3)
        }
        estimator = SVC()
        search = RandomizedSearchCV

    # create pipeline
    pipe = make_pipeline(
        preprocessor, estimator
    )

    # Hyperparameter optimization
    random_search = search(
        pipe, 
        param_dist,
        cv=5,
        return_train_score=True
    )
    
    return random_search


def save_files(model_name, random_search, out_dir, X_test, y_test):
    """
    """
    if model_name == 'knn':
        param_lst = [
        'param_kneighborsclassifier__n_neighbors'
    ]
    else:
        param_lst = [
            'param_svc__alpha',
            'param_svc__gamma'
        ]

    # columns from CV we want to keep
    col_lst = param_lst + [
        'mean_fit_time',
        'mean_score_time',
        'mean_test_score',
        'std_test_score',
        'mean_train_score',
        'std_train_score'
        ]

    # file names
    search_cv_filename = model_name + '_randsearch_cv_results.csv'
    best_model_filename = 'best_' + model_name + '.pickle'
    conf_matrx_filename = model_name + 'confusion_matrix.png'
    test_score_filename = model_name + '_test_score.csv'

    # save cv results from HP optimization
    pd.DataFrame(
        random_search.cv_results_
    ).set_index('rank_test_score').sort_index()[
        col_lst
        ].round(3).to_csv(os.path.join(out_dir, search_cv_filename))

    # find best model
    best_model = random_search.best_estimator_

    # score best model on test data and save
    pd.DataFrame(
        [best_model.score(X_test, y_test)], 
        columns=[model_name]
    ).to_csv(os.path.join(out_dir, test_score_filename), index=False)
    
    # save the best model
    with open(os.path.join(out_dir, best_model_filename), 'wb') as model_file:
        pickle.dump(best_model, model_file, protocol = pickle.HIGHEST_PROTOCOL)

    # create confusion matrix and save
    cm = ConfusionMatrixDisplay.from_estimator(
        best_model, 
        X_test, 
        y_test, 
        values_format = 'd',
        xticks_rotation='vertical'
    )

    cm.figure_.savefig(os.path.join(out_dir, conf_matrx_filename), bbox_inches='tight')


def main(model, in_dir, out_dir):
    
    # make results directory
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # read in the data
    X_train, y_train = get_data_splits(in_dir, train=True)
    X_test, y_test = get_data_splits(in_dir, train=False)
    
    # create preprocessor, may need column names
    categorical_variables = ['TYPE2', 'COLOR', 'ABILITY1', 'ABILITY2', 'ABILITY HIDDEN']
    numeric_variables = ['HEIGHT', 'WEIGHT', 'HP', 'ATK', 'DEF', 'SP_ATK', 'SP_DEF', 'SPD']
    passthrough_variables = ['LEGENDARY', 'MEGA_EVOLUTION']
    drop_variables = ['NUMBER', 'CODE', 'SERIAL', 'NAME', 'GENERATION', 'TOTAL']

    preprocessor = make_column_transformer(
        (OneHotEncoder(handle_unknown='ignore'), categorical_variables),
        (StandardScaler(), numeric_variables),
        ('passthrough', passthrough_variables),
        ('drop', drop_variables)
    )

    if model == 'both':
        for sep_model in ['knn', 'svc']:

            # perform the hyperparameter optimization
            random_search = get_pipe_search(sep_model, preprocessor)
            random_search.fit(X_train, y_train)

            save_files(sep_model, random_search, out_dir, X_test, y_test)

    else:
        # perform the hyperparameter optimization
        random_search = get_pipe_search(model, preprocessor)
        random_search.fit(X_train, y_train)

        save_files(sep_model, random_search, out_dir, X_test, y_test)


if __name__ == "__main__":
    try:
        opt = docopt(__doc__)
        main(opt["--model"], opt["--inp_dir"], opt["--out_dir"])
    except DocoptExit:
        print(__doc__)
    