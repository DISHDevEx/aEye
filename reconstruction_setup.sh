#!/bin/sh

activate base

apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
conda update -n base -c defaults conda -y
conda install pytorch==1.7.1 torchvision==0.8.2 torchaudio==0.7.2 cudatoolkit=10.1 -c pytorch -y 

python3 -m pip install openmim
python3 -m mim install mmcv-full
python3 -m pip install mmedit