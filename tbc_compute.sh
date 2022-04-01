#!/bin/bash

python3 tbc_compute.py \
 -ri 179.62 -0.392 -90 \
 -ti 0.0827 0.0225 0.0425 \
 -rc -0.24558 0.213438 90 \
 -tc -0.1093 0 0.063 \
 "$@"

# python3 tbc_compute.py \
#  -ri 180 0 -90 \
#  -ti 0.0827 0.0225 0.0425 \
#  -rc 0 0 90 \
#  -tc -0.1093 0 0.063 \
#  "$@"