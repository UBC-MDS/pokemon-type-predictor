FROM continuumio/miniconda3

# install some dependencies
RUN apt-get update --fix-missing \
	&& apt-get install -y \
		ca-certificates \
    	libglib2.0-0 \
	 	libxext6 \
	   	libsm6  \
	   	libxrender1 \
		libxml2-dev \
        gcc \
        make \
        pandoc \
        pandoc-citeproc

# Install base R and devtools
RUN apt-get install wget r-base r-base-dev -y 

# install python3 & virtualenv
RUN apt-get install -y \
		python3-pip \
		python3-dev 

# install conda dependencies
RUN conda config --add channels conda-forge
RUN conda install -y pip \
        pandas=1.4.4 \
        altair=4.2.0 \
        requests=2.24.0

# install pip dependencies
RUN pip install --upgrade pip \
    docopt-ng \
    vl-convert-python \
    matplotlib \
    altair-saver==0.5.0 \
    scikit-learn==1.1.3 \
    selenium==4.2.0 \
    && rm -fr /root/.cache

ENV LD_LIBRARY_PATH /usr/local/lib/R/lib/:${LD_LIBRARY_PATH}

# install R packages
RUN Rscript -e "install.packages('knitr')" 
RUN Rscript -e "install.packages('rmarkdown')"