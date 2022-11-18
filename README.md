# Pokemon Type Predictor
Authors: Sarah Abdelazim, Wilfred Hass, Vincent Ho, Caroline Tang
---
# Proposal
### Dataset
https://gist.github.com/simsketch/1a029a8d7fca1e4c142cbfd043a68f19
https://gist.github.com/HansAnonymous/56d3c1f8136f7e0385cc781cf18d486c - cleaned version
### 1. Background info (on pokemon and stats)
Pokemon as a popular video game series
In main series, use pokemon to fight each other in turn-based battles to become the champion of a region
Pokemon have different elemental types (18 total) (eg water, fire, grass, electric, steel) which determine their strengths and weaknesses to attacks, which also have types
Each new game in the series introduces new pokemon, which, when first encountered in the game, usually gives no indication to its type -> question?

### 2. Question
Can we predict a pokemon’s type based on its other attributes?
This question has been done before but usually only focusing on stats only, we have stats + ability/abilities + color

### 3. EDA
Split the data 70%/30% before doing EDA since we have a predictive research question.

Figures: 
- distributions of stats, correlations between stats?
- use alt.repeat to see the distributions of numerical and categorical features. (altair)

Tables:
-  counts of abilities, color, etc.
-  use a correlation table to see the correlation between numerical variables. (pandas, matplotlib)

	How these EDA helps us to determine which columns should be dropped

### 4. Analysis
Classifier model
SVC?
kNN?

### 5. How to share the results of analysis
Table/Figures:
- confusion matrix, classification report

# Usage

# Licenses


# References (if any)