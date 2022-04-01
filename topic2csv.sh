#!/bin/bash

python3 topic2csv.py \
 ../data/0382-frames/LocalPoseTopic.txt \
 -k attRate acc \
 "$@"
