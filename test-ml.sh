#!
export TF_ENABLE_ONEDNN_OPTS=0
python -m unittest discover -s "src/ml_test" -p "*_.py"
