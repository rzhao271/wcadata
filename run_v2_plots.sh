#!/bin/sh

# This file runs the newer plots
python quartiles_singles.py
python quartiles_averages.py
python solver_counts_averages.py
python solver_counts_singles.py
