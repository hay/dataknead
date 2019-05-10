#!/bin/bash
rm output/*

for file in *_example.py; do
    echo "Executing "$file
    python $file
    echo ""
done