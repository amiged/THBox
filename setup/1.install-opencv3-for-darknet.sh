#!/bin/bash

echo 'for Ubuntu 16.04.2 LTS'

# ------------------------
# Dependences
# ------------------------
sudo apt install -y gcc g++ git libjpeg-dev libpng-dev libtiff5-dev libjasper-dev \
		 libavcodec-dev libavformat-dev libswscale-dev pkg-config libgtk2.0-dev \
		 libeigen3-dev libtheora-dev libvorbis-dev libxvidcore-dev libx264-dev sphinx-common \
		 libtbb-dev yasm libfaac-dev libopencore-amrnb-dev libopencore-amrwb-dev libopenexr-dev \
		 libgstreamer-plugins-base1.0-dev libavcodec-dev libavutil-dev libavfilter-dev \
		 libavformat-dev libavresample-dev libgphoto2-6 libgphoto2-dev libdc1394-22-dev libdc1394-22 libdc1394-utils \
		 build-essential
sudo apt-get build-dep opencv
sudo apt install libvtk6-qt-dev libgoogle-glog-dev
sudo apt -y install mplayer ffmpeg

# ------------------------
# cmake
# ------------------------
wget https://cmake.org/files/v2.8/cmake-2.8.12.2.tar.gz
tar xzvf cmake-2.8.12.2.tar.gz
cd cmake-2.8.12.2;
./bootstrap;
make -j;
sudo make install
cd ..

# ------------------------
# Opencv 3.2 for CUDA
# ------------------------
#wget https://github.com/opencv/opencv/archive/3.2.0.zip
#unzip 3.2.0.zip
#wget https://raw.githubusercontent.com/opencv/opencv_3rdparty/81a676001ca8075ada498583e4166079e5744668/ippicv/ippicv_linux_20151201.tgz -P ./opencv-3.2.0/3rdparty/ippicv/downloads/linux-808b791a6eac9ed78d32a7666804320e

#mkdir -p opencv-3.2.0/release
#cd opencv-3.2.0;
#cd release;
#time cmake -DBUILD_TIFF=ON -DBUILD_opencv_java=OFF -DWITH_CUDA=ON -DENABLE_AVX=ON -DWITH_OPENGL=ON -DWITH_OPENCL=ON -DWITH_TBB=ON -DWITH_EIGEN=ON -DWITH_V4L=ON -DWITH_VTK=OFF -DBUILD_TESTS=OFF -DBUILD_PERF_TESTS=OFF -DCMAKE_BUILD_TYPE=RELEASE -DBUILD_opencv_python2=OFF -DCMAKE_INSTALL_PREFIX="$HOME/anaconda3" -DPYTHON3_EXECUTABLE="$HOME/anaconda3/bin/python3" -DPYTHON3_INCLUDE_DIR="$HOME/anaconda3/include/python3.6m" -DPYTHON3_PACKAGES_PATH="$PATH/anaconda3/lib/python3.6/site-packages" ..
#cd ../../

python3 -c "import sys; print(sys.prefix)" #  -DCMAKE_INSTALL_PREFIX 
python3 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())" # -DPYTHON3_INCLUDE_DIR
python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())" # -DPYTHON3_PACKAGES_PATH
unzip ./tar/3.2.0.zip
mkdir -p ./opencv-3.2.0/3rdparty/ippicv/downloads/linux-808b791a6eac9ed78d32a7666804320e
rsync -av ./tar/ippicv_linux_20151201.tgz ./opencv-3.2.0/3rdparty/ippicv/downloads/linux-808b791a6eac9ed78d32a7666804320e/
mkdir -p opencv-3.2.0/release
cd opencv-3.2.0/release;
time cmake -DBUILD_TIFF=ON -DBUILD_opencv_java=OFF -DWITH_CUDA=OFF -DENABLE_AVX=ON -DWITH_OPENGL=ON -DWITH_OPENCL=OFF -DWITH_TBB=ON -DWITH_EIGEN=ON -DWITH_V4L=ON -DWITH_VTK=OFF -DBUILD_TESTS=OFF -DBUILD_PERF_TESTS=OFF -DCMAKE_BUILD_TYPE=RELEASE -DBUILD_opencv_python2=OFF \
    -DCMAKE_INSTALL_PREFIX=/usr/local  \
    -DPYTHON3_EXECUTABLE=/usr/bin/python3 \
    -DPYTHON3_INCLUDE_DIR=/usr/include/python3.5m \
    -DPYTHON3_PACKAGES_PATH=/usr/lib/python3/dist-packages
		..
cd ../../

# ------------------------
# make instasll
# ------------------------
cd opencv-3.2.0/release;
make -j;
sudo make install


# python numpy
sudo apt install python3-pip
pip3 install --upgrade pip
pip3 install numpy

