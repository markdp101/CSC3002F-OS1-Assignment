#!/bin/bash

# Clean all files.
make clean
rm -f *raw_data*.txt *Plot.txt

# Compile program.
make

# Run the simulation 3 times, each time with a different scheduling algorithm:
# Number of patrons = 50 (Should set to 100 for actual runs)
# Scheduler = [0, 1, 2] ([FCFS, SJF, RR])
# Context switch = 1 (Must still be experimented with)
# Time quantum = 70 (Must still be experimented with)
# Random seed = 5
# for i in 0 1 2 3 4 5 6 7 8 9
for i in 0 1 2
do
    for j in 0 1 2
    do
        make run ARGS="100 ${j} 1 70 5" > scheduler_${j}_raw_data_${i}.txt
    done
done

python3 dataprocessing.py