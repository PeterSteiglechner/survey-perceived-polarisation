#!/bin/bash

# create and activate virtual environment
python -m venv otree-env
source otree-env/bin/activate

# upgrade pip
pip install --upgrade pip

# install otree >=5.11.1
pip install "otree>=5.11.1"
pip install numpy matplotlib pandas scipy

