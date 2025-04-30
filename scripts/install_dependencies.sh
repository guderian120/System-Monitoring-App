#!/bin/bash
# Install required dependencies
apt-get update
apt-get install -y python3 python3-pip
pip3 install prometheus-client psutil