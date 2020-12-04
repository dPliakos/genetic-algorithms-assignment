#!/bin/bash

echo "Running script $1"
./.venv/bin/python3 ./src/main.py > "./output/out$1.txt";
