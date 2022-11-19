# Pokemon Type Predictor

## Authors

### Gym Leaders (Original Team)

- Caroline Tang
- Sarah Abdelazim
- Vincent Ho
- Wilfred Hass

### Gym Trainers (Contributors)

Data analysis project created in part of requirements for DSCI 522 (Data Science Workflows); a course in the Master of Data Science program at the University of British Columbia.

## Introduction

Originally developed as a video game, the hit 90's pop culture franchise Pokemon flourished into multiple media streams. As was big in the 90's, Pokemon took over the trading card industry and even turned into a television show that rocked the world.

Pokemon (the creatures) share the same name as the title of the franchise. These creatures come in a variety of shapes, sizes, and colours; some modelled after animals or objects in the real world and some as fantastic beasts from the creator's imagination. Trainers in the game go around collecting Pokemon and using them to do battle. The Pokemon gain experience through these battles and can evolve into new creatures. Each Pokemon has specific attributes that allow them to beat other ones. Some attributes are categorical such as their type (water, rock, air, etc.) and some attributes are numerical, such as their speed, attack or defense. A combination of these attributes (and a little luck) are what determines if a Pokemon will either win a battle or lose.

As a way to keep children attentive to the show and more familiar with the franchise, the show often asked the famous question "Who's that Pokemon?!" at the beginning of a commercial break, with an image of the shaded outline of a Pokemon. The show would reveal the Pokemon at the end of the commercial break, rewarding those who stayed through the advertisements.

Initially inspired by this ploy of the franchise, we thought it might be interesting to predict something related to the Pokemon. This thought was further developed when we remembered that as each generation of the franchise is released, the players encounter brand new Pokemon that the world has never seen. When encountering a new Pokemon, the game gives no indication to its type, leading us to our question: given the attributes of an undiscovered Pokemon, are we able to predict its type?

## Data

While this question has been done before using only the statistics (Note: we use the term "statistics" to describe the attributes related to a given Pokemon) of each Pokemon, we now have a dataset that includes the ability(ies) of the Pokemon and its color as well. We aim to use these in our classification. The data is found [here](https://gist.github.com/HansAnonymous/56d3c1f8136f7e0385cc781cf18d486c). The data was cleaned by [HansAnonymous](https://gist.github.com/HansAnonymous) and originally developed by [simsketch](https://gist.github.com/simsketch). The original data can be found in the [Pokemon database](https://pokemondb.net/pokedex). All rights belong to their respective owners.

Each row in the dataset contains a different Pokemon with various attributes. The attributes are measurements of the base Pokemon, such as `attack`, `speed` or `defense`.

The different types of Pokemon are closely related to the other attributes it possesses. For example, a rock type Pokemon is likely to have higher defensive statistics (such as `defense` or `health points`) as well as rock-type abilities. It is also most likely to be coloured grey. To complicate this even further, there are some Pokemon with more than one type, such as Pidgey, who has both `Normal` and `Flying` types. We can use this to our advantage by using the second type as a feature that may lead to discovering the first type.

## Exploratory Data Analysis

Before exploring the data, we will first fill the second types of the Pokemon with `N/A` values. Then, we will shuffle and split the dataset into 70% training data and 30% testing data. We plan exploring the training data to find the distribution of statistics for the different Pokemon types, along with the correlations between any statistics. We can plot these distributions using [altair](https://altair-viz.github.io/).

We will also create tables to explore the various categorical columns such as  the number of distinct colours of Pokemon or the distinct abilities that exist. We will also use tables to see any correlation between numerical features.

These explorations will help us determine if any features should be dropped and how we will need to preprocess them.

## Analysis

We will attempt to use various classification models to predict the Pokemon types. The models will be implemented using [sklearn](https://scikit-learn.org/stable/index.html). Some such models that are considered are:

- Support Vector Classifier (SVC)
- $k$ - Nearest Neighbours ($k$-NN)
- Logistic Regression

The models each have their own set of hyperparameters that will have to be optimized using cross-validation. We will use average accuracy as the metric to determine each of these hyperparameters and show plots of the accuracy and hyperparameters to determine the best ones.

## Results

Once the best hyperparameters are chosen, we will determine which model is the best and refit that model to our training data. We will attempt to evaluate our model on the test data and use confusion matrices as well as other metrics such as precision and recall to see how our model did. We will also look at the soft predictions, i.e. how confident our model is in each prediction and choose the top two. These two will be the predicted possible types for a new Pokemon. We are using soft predictions to measure the confidence as well as to see if the Pokemon will have multiple types. These metrics and classification reports will be available in the final report.

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

To download the data, ensure that you have a `data/raw` folder in the parent directory. Then, use the command:

```console
python 
```

To run the EDA, please open the EDA file in the `src` directory and run all the cells.

## License

The Pokemon Type Predictor materials here are licensed under the Creative Commons Attribution 2.5 Canada License (CC BY 2.5 CA).

## Attributions

We attribute the creation of the `license` file to Tiffany Timbers, with more information available in the `license` file.

The data is attributed to the GitHub users: [HansAnonymous](https://gist.github.com/HansAnonymous/56d3c1f8136f7e0385cc781cf18d486c), [simsketch](https://gist.github.com/simsketch) and the online [Pokemon database](https://pokemondb.net/pokedex).
