# !bin/bash

read -p "Please enter the Python version you want to use (e.g., 3.9): " PYTHON_VERSION

conda create --name dependency-mock python=$PYTHON_VERSION -y

conda activate dependency-mock

pip install -r requirements.txt

