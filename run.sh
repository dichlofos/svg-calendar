#!/usr/bin/env bash
for i in $(seq 1 12); do
    python ./sc.py $i > cal$i.svg
    convert -resample 600 cal$i.svg cal$i.png
done
