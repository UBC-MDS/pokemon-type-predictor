"""Cleans and preprocesses pokemon data (https://gist.githubusercontent.com/HansAnonymous/56d3c1f8136f7e0385cc781cf18d486c/raw/f91faec7cb2fd08b3c28debf917a576c225d8174/pokemon.csv) in preparation for model implementation.
Splits the data into train and test sets, writes them and saves them to csv files.

Usage: preprocessing.py --input_file=<input_file> --out_dir=<out_dir> 
 
Options:
--input_file=<input_file>       Path (including filename) to raw data (csv file)
--out_dir=<out_dir>             Path of where to locally write the file
"""

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from docopt import docopt

opt = docopt(__doc__)

def main(input_file, out_dir):
    
    #reads input file
    data = pd.read_csv(input_file)
    
    #adds missing values of TYPE2 column from TYPE1 column
    data['TYPE2'] = data['TYPE2'].fillna(data['TYPE1'])
    
    #adds missing values of ABILITY2 column from ABILITY1 column
    data['ABILITY2'] = data['ABILITY2'].fillna(data['ABILITY1'])
    
    #adds missing values of ABILITY HIDDEN column from ABILITY1 column
    data['ABILITY HIDDEN'] = data['ABILITY HIDDEN'].fillna(data['ABILITY1'])
    
    #splits the data into train and test sets
    train_df, test_df = train_test_split(data, test_size=0.3, random_state=123)
    
    #writes the train and test csv files and saves them
    try:
        train_df.to_csv(os.path.join(out_dir, "train.csv"), index=False)
        test_df.to_csv(os.path.join(out_dir, "test.csv"), index=False)
    except:
        os.makedirs(os.path.dirname(out_dir))
        train_df.to_csv(out_dir + "train.csv", index=False)
        test_df.to_csv(out_dir + "test.csv", index=False)

if __name__ == "__main__":
    main(opt["--input_file"], opt["--out_dir"])
