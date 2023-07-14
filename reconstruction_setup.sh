#!/bin/sh
activate base
pip install torch torchvision torchaudio 
pip install openmim
mim install mmcv-full
pip install mmedit
apt-get update && apt-get install ffmpeg libsm6 libxext6  -y