#!/usr/bin/env bash
y="2016"
mkdir -p "$y"
for i in $(seq 1 12); do
    python ./sc.py $y $i > $y/cal-$i.svg
    convert -resample 600 $y/cal-$i.svg $y/cal-$i.png
done
