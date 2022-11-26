# Pokemon Type Predictor

## Authors

### Gym Leaders (Original Team)

- Caroline Tang
- Sarah Abdelazim
- Vincent Ho
- Wilfred Hass

### Gym Trainers (Contributors)

Data analysis project created in part of requirements for DSCI 522 (Data Science Workflows); a course in the Master of Data Science program at the University of British Columbia.

## About

In this project, we attempt to build a classification model using two algorithms: $k$ - Nearest Neighbours and a Support Vector Machine. We will use this classification model to classify a Pokemon's type (of which there are 18 possible types) based on the other stats (such as attack, defense, etc.) that it has. We use accuracy as the metric to score our models since there is no detriment to false positives or negatives, but we do want to know how many of the unknown Pokemon will be predicted correctly. On the unseen test data, the $k$ -NN model predicted 60% of the new Pokemon correctly while the SVC model predicted 67% correctly. Since these are not very accurate results, we recommend trying different estimators to fill up that Pokedex!

## Data

The data is found [here](https://gist.github.com/HansAnonymous/56d3c1f8136f7e0385cc781cf18d486c). The data was cleaned by [HansAnonymous](https://gist.github.com/HansAnonymous) and originally developed by [simsketch](https://gist.github.com/simsketch). The original data can be found in the [Pokemon database](https://pokemondb.net/pokedex). All rights belong to their respective owners.

Each row in the dataset contains a different Pokemon with various attributes. The attributes are measurements of the base Pokemon, such as `attack`, `speed` or `defense`.The different types of Pokemon are closely related to the other attributes it possesses. For example, a rock type Pokemon is likely to have higher defensive statistics (such as `defense` or `health points`) as well as rock-type abilities. It is also most likely to be coloured grey.

## Report
The final report is available [here](/doc/final_report.md)

## Usage

To replicate the analysis, first clone this GitHub repository. Then, install `nb_conda_kernels` in you **base** environment. Now, install the dependencies listed in the `env-poke-type-pred.yaml` file below as an Anaconda environment, using:

```console
conda install -c conda-forge nb_conda_kernels
conda env create -f env-poke-type-pred.yaml
```

You can switch to this environment using:

```console
conda activate poketype
```

To download the data so that it works with our analysis, ensure you are in the parent directory in your terminal. Then, use the command:

```console
python src/download-data.py --url=https://gist.githubusercontent.com/HansAnonymous/56d3c1f8136f7e0385cc781cf18d486c/raw/f91faec7cb2fd08b3c28debf917a576c225d8174/pokemon.csv --out_file=data/raw/pokemon.csv
```

To process and split the data after downloading it above, you can run the following command:

```console
python src/preprocessing.py --input_file=data/raw/pokemon.csv --out_dir=data/processed/
```

To run the EDA, you can use the following command:

```console
python src/pokemnon_eda.py --train=data/processed/train.csv --out_dir=results/eda/
```

Then, to run the statistical models, you can use the following command. To run all the models, use `--model=all`, otherwise you can specify with `dummy`, `knn`, or `svc`.

```console
python src/poke_training.py --model=all --train=data/processed/ --out_dir=results/
```

To reproduce the final report, please run:

```console
Rscript -e "rmarkdown::render('src/final_report.Rmd')"
```

## License

The Pokemon Type Predictor materials here are licensed under the Creative Commons Attribution 2.5 Canada License (CC BY 2.5 CA).

## Attributions

We attribute the creation of the `license` file to Tiffany Timbers, with more information available in the `license` file.

The data is attributed to the GitHub users: [HansAnonymous](https://gist.github.com/HansAnonymous/56d3c1f8136f7e0385cc781cf18d486c), [simsketch](https://gist.github.com/simsketch) and the online [Pokemon database](https://pokemondb.net/pokedex).
