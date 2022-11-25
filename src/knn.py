"""
Fits, optimizes a k-NN model on training data, then scores it on the test data.
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
from docopt import docopt

opt = docopt(__doc__)

def main(input_dir, out_dir):


if __name__ == "__main__":
    main(opt["--input_dir"], opt["--out_dir"])