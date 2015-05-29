#!/usr/bin/env bash
for i in $(seq 1 12); do
    python ./sc.py $i > cal$i.svg
done
