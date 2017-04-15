#!/usr/bin/env bash

# Configure EC2 instances for storage performance data collection

sudo yum -y update
sudo yum -y install git
sudo yum -y group install "Development Tools"
sudo yum -y install zlib-devel libaio-devel
git clone https://github.com/axboe/fio.git
cd fio
./configure
make -j 3
sudo make install
cd
git clone https://github.com/FreshetDMS/FDCapacityPlanner.git

if [ -e '/dev/xvdca' ]; then
    sudo mkfs -t ext4 /dev/xvdca
    sudo mkdir -p /media/disk1
    sudo mount /dev/xvdca /media/disk1
fi

if [ -e '/dev/xvdba' ]; then
    sudo mkfs -t ext4 /dev/xvdba
    sudo mkdir -p /media/disk1
    sudo mount /dev/xvdba /media/disk1
fi

