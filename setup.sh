#!
# Source this file. Don't let it spawn a new shell.

python3 -m pip install --upgrade pip && \
    python3 -m venv venv && \
    . ./venv/bin/activate && \
    pip install -r requirements.txt
