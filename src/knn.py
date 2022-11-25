"""
Optimizes and fits a k-NN model on training data, then scores it on the test data.
Usage: knn.py --input_dir=<input_dir> --out_dir=<out_dir> 
 
Options:
--input_dir=<input_dir>         Path to processed data folder
--out_dir=<out_dir>             Path to folder in which to download results
"""

import os
import numpy as np
import pandas as pd
from scipy.stats import randint
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.model_selection import cross_validate, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import pickle
from docopt import docopt

opt = docopt(__doc__)

def main(input_dir, out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # read in data and split into X and y
    train_df = pd.read_csv(os.path.join(input_dir, 'train.csv'))
    X_train, y_train = train_df.drop(columns=['TYPE1']), train_df['TYPE1']

    # create preprocessor
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

    # create pipeline
    knn_pipe = make_pipeline(
        preprocessor, KNeighborsClassifier()
    )

    # hyperparameter (k) optimization
    param_grid = {
        'kneighborsclassifier__n_neighbors': range(1, 20)
    }
    random_search = GridSearchCV(
        knn_pipe, 
        param_grid,
        cv=5,
        return_train_score=True
    )
    random_search.fit(X_train, y_train)

    #save cv results
    pd.DataFrame(
        random_search.cv_results_
    ).set_index('rank_test_score').sort_index()[[
        'param_kneighborsclassifier__n_neighbors',
        'mean_fit_time',
        'mean_score_time',
        'mean_test_score',
        'mean_train_score'
    ]].to_csv(os.path.join(out_dir, 'knn_cv_results.csv'))

    # save best model
    best_model = random_search.best_estimator_
    with open(os.path.join(out_dir, 'best_knn.pickle'), 'wb') as model_file:
        pickle.dump(best_model, model_file, protocol = pickle.HIGHEST_PROTOCOL)

    # read in test data
    test_df = pd.read_csv(os.path.join(input_dir, 'test.csv'))
    X_test, y_test = test_df.drop(columns = ['TYPE1']), test_df['TYPE1']

    # score model on test data and save
    pd.DataFrame(
        [best_model.score(X_test, y_test)], 
        columns=['knn']
    ).to_csv(os.path.join(out_dir, 'knn_test_score.csv'), index=False)

    # create confusion matrix and save
    cm = ConfusionMatrixDisplay.from_estimator(
        best_model, 
        X_test, 
        y_test, 
        values_format = 'd',
        xticks_rotation='vertical'
    )

    cm.figure_.savefig(os.path.join(out_dir, 'knn_confusion_matrix.png'), bbox_inches='tight')


if __name__ == "__main__":
    main(opt["--input_dir"], opt["--out_dir"])