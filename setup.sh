#!
# Source this file. Don't let it spawn a new shell.

if [[ "$OSTYPE" == "linux-gnu"* ]]; then  # Linux
    echo "OS environment: Linux GNU"
    python3 -m pip install --upgrade pip && \
        python3 -m venv venv && \
        . ./venv/bin/activate && \
        python3 -m pip install --upgrade pip && \
        pip install -r requirements.txt

elif [[ "$OSTYPE" == "msys"* ]]; then  # GitBash
    echo "OS environment: MinGW"
    python -m pip install --upgrade pip && \
        python -m venv venv && \
        . ./venv/Scripts/activate && \
        python -m pip install --upgrade pip && \
        pip install -r requirements.txt
else
    echo "Unknown OS environment"
fi