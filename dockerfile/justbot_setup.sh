#!/bin/bash
source /opt/ros/noetic/setup.bash

cd ~/catkin_ws && catkin_make
source devel/setup.bash

sudo pip3 install pyyaml

git clone https://github.com/armgits/justbot.git ~/catkin_ws/src/justbot_project

sudo rm -rf ~/cakin_ws/src/justbot_project/cad/ \
  ~/cakin_ws/src/justbot_project/code/ \
  ~/cakin_ws/src/justbot_project/dockerfile/ \
  ~/cakin_ws/src/justbot_project/image/ \
  ~/cakin_ws/src/justbot_project/README.md

sudo chmod +x ~/catkin_ws/src/justbot_project/justbot/src/move.py
sudo chmod +x ~/catkin_ws/src/justbot_project/justbot/src/start.py

cd ~/catkin_ws
catkin_make clean && catkin_make
source ~/catkin_ws/devel/setup.bash
