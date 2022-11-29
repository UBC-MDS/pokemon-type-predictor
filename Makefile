# Makefile
# Author: Wilfred Hass, Caroline Tang, Vincent Ho, Sarah Abdelazim
# Date: 2022-11-30

# all : doc/final_report.html 

all : doc/final_report.html doc/final_report.md

clean : 
	rm -rf data/*
	rm -rf results/*
	rm -f doc/final_report.html
	rm -f doc/final_report.md

# download raw data
data/raw/pokemon.csv : src/download_data.py
	python src/download_data.py --url=https://gist.githubusercontent.com/HansAnonymous/56d3c1f8136f7e0385cc781cf18d486c/raw/f91faec7cb2fd08b3c28debf917a576c225d8174/pokemon.csv --out_file=data/raw/pokemon.csv

# processing data
data/processed/train.csv data/processed/test.csv : data/raw/pokemon.csv src/preprocessing.py
	python src/preprocessing.py --input_file=data/raw/pokemon.csv --out_dir=data/processed/

# eda files
results/eda/EDA_ability_vs_type1.png results/eda/EDA_correlation.png results/eda/EDA_data_description.png results/eda/EDA_dist_of_cat.png results/eda/EDA_dist_of_num.png results/eda/EDA_type1_vs_color.png : data/processed/train.csv src/pokemon_eda.py
	python src/pokemon_eda.py --train=data/processed/train.csv --out_dir=results/eda/

# Model files
results/dummy/best_dummy.pickle results/dummy/dummy_confusion_matrix.png results/dummy/dummy_randsearch_cv_results.csv results/dummy/dummy_test_score.csv : data/processed/train.csv data/processed/test.csv src/poke_training.py
	python src/poke_training.py --model=dummy --in_dir=data/processed/ --out_dir=results/

results/knn/best_knn.pickle results/knn/knn_confusion_matrix.png results/knn/knn_randsearch_cv_results.csv results/knn/knn_test_score.csv : data/processed/train.csv data/processed/test.csv src/poke_training.py
	python src/poke_training.py --model=knn --in_dir=data/processed/ --out_dir=results/

results/svc/best_svc.pickle results/svc/svc_confusion_matrix.png results/svc/svc_randsearch_cv_results.csv results/svc/svc_test_score.csv : data/processed/train.csv data/processed/test.csv src/poke_training.py
	python src/poke_training.py --model=svc --in_dir=data/processed/ --out_dir=results/

# Render final report
doc/final_report.html : results/eda/EDA_correlation.png results/dummy/dummy_confusion_matrix.png results/knn/knn_confusion_matrix.png results/svc/svc_confusion_matrix.png doc/pokeref.bib
	Rscript -e "rmarkdown::render('doc/final_report.Rmd')"

doc/final_report.md : results/eda/EDA_correlation.png results/dummy/dummy_confusion_matrix.png results/knn/knn_confusion_matrix.png results/svc/svc_confusion_matrix.png doc/pokeref.bib
	Rscript -e "rmarkdown::render('doc/final_report.Rmd', output_format = 'github_document')"