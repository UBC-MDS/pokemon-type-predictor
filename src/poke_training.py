"""
Optimize and fits either kNN, SVC or both models on training data. Scores it on the test data,
then produces CV scores, test scores and confusion matrices as files in /results
Usage: run_model.py --model=<model> --in_dir=<in_dir> --out_dir=<out_dir> 
 
Options:
--model=<model>           Model to run (dummy | knn | svc | all)
--in_dir=<in_dir>         Path to processed data folder
--out_dir=<out_dir>       Path to folder in which to export the results

Arguments:
    model:  dummy - Dummy classifier model
            knn - kNN model
            svc - SVC model
            all - runs all models above
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
from sklearn.dummy import DummyClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import pickle
from docopt import docopt, DocoptExit


def get_data_splits(in_dir, train=True):
    """ 
    Splits either `train` or `test` data into its features/values and labels

    Parameters:
    ------
    in_dir:        (str)  path to processed data
    train:         (bool) Sets the csv filename for which type of data we need

    Returns:
    ------
    X:             (pd DataFrame) dataframe containing the relevant features and values
    y:             (pd DataFrame) dataframe containing the relevant labels
    """
    if train:
        data_type = 'train.csv'
    else:
        data_type = 'test.csv'            
    df = pd.read_csv(os.path.join(in_dir, data_type))
    
    # split into features/values and labels
    X, y = df.drop(columns=['TYPE1']), df['TYPE1']
    return X, y


def get_search(model, preprocessor):
    """ 
    Creates the search object needed to optimize the hyperparameters.
    Has predefined distributions used for each model.

    Parameters:
    ------
    model:          (str) name of the estimator to run
    preprocessor:   (column_transformer) preprocessor with the relevant transformations

    Returns:
    ------
    search object from `RandomizedSearchCV`
    """
    # decide the model and relevant hyperparameters to optimize
    if model == 'knn':
        param_dist = {
        'kneighborsclassifier__n_neighbors': list(range(1, 21))
        }
        estimator = KNeighborsClassifier()

    elif model == 'svc':
        param_dist = {
        "svc__gamma": loguniform(1e-2, 1e3),
        "svc__C": loguniform(1e-2, 1e3)
        }
        estimator = SVC()

    elif model == 'dummy':
        param_dist = {}
        estimator = DummyClassifier()

    # create pipeline
    pipe = make_pipeline(
        preprocessor, estimator
    )

    # define the hyperparameter optimization
    random_search = RandomizedSearchCV(
        pipe, 
        param_dist,
        n_iter=50,
        cv=5,
        return_train_score=True,
        random_state=123
    )
    
    return random_search


def save_files(model_name, random_search, out_dir, X_test, y_test):
    """ 
    Saves a csv of the search's CV scores, a csv of the best model 
    on the test set, a pickle copy of the best model and the confusion matrix
    produced by the best model.

    Parameters:
    ------
    model_name:     (str)                name of the estimator being run, for filepaths
    random_search:  (RandomizedSearchCV) Search object that has already been trained
    out_dir:        (str)                name of the output directory to save the files
    X_test:         (pd DataFrame)       Dataframe containing the testing features and values
    y_test:         (pd DataFrame)       Dataframe containing the testing labels
    """

    out_dir = os.path.join(out_dir, model_name)

    # make results directory
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    if model_name == 'knn':
        param_lst = ['param_kneighborsclassifier__n_neighbors']
    elif model_name == 'svc':
        param_lst = ['param_svc__C', 'param_svc__gamma']
    else:
        param_lst = []

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
    search_cv_filename =  model_name + '_randsearch_cv_results.csv'
    best_model_filename = 'best_' + model_name + '.pickle'
    conf_matrx_filename = model_name + '_confusion_matrix.png'
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
    """
    Wrapper function to carry out the script pipeline

    Parameters:
    ------
    model:      (str)   name of estimator to be tested
    in_dir:     (str)   path to the processed data directory (not including filenames)
    out_dir:    (str)   path to the results directory
    """
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

    if model == 'all':
        for sep_model in ['dummy', 'knn', 'svc']:

            # perform the hyperparameter optimization
            random_search = get_search(sep_model, preprocessor)
            random_search.fit(X_train, y_train)

            save_files(sep_model, random_search, out_dir, X_test, y_test)

    else:
        # perform the hyperparameter optimization
        random_search = get_search(model, preprocessor)
        random_search.fit(X_train, y_train)

        save_files(model, random_search, out_dir, X_test, y_test)


if __name__ == "__main__":
    try:
        opt = docopt(__doc__)
        main(opt["--model"], opt["--in_dir"], opt["--out_dir"])
    except DocoptExit:
        print(__doc__)