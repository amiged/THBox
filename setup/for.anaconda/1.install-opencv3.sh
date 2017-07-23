#!/bin/bash
#Time-stamp: <2017-07-04 18:59:11 hamada>

#conda install -c https://conda.binstar.org/menpo opencv3
conda install -c https://conda.anaconda.org/menpo opencv3

pip install fasteners

anaconda search -t conda ffmpeg
conda install -c conda-forge ffmpeg=3.2.4


