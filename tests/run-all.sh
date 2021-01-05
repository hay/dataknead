#!/bin/bash

# Note that you probably want to run this using poetry
# e.g poetry run ./run-all.sh
rm output/*

for file in *_example.py; do
    echo "Executing "$file
    python $file
    echo ""
done