#!/bin/bash

# Read environment variables from config.conf
SCRIPT_DIR="./vscode_remote_debugging"
while read var value
do
    export "$var"="$value"
done < $SCRIPT_DIR/config.conf

cd $WORKDIR

# Activate conda environment
source $CONDA_SOURCE
conda activate $CONDA_ENV

echo Waiting for debugger to attach...

# Run script
python -m debugpy --listen 0.0.0.0:$PORT --wait-for-client $WORKDIR/main.py  --cuda --wait-time 7

conda deactivate