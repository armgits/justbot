#!/bin/bash
source /opt/ros/noetic/setup.bash

cd ~/catkin_ws && catkin_make
source devel/setup.bash
sudo pip3 install pyyaml

cd ~/catkin_ws/src
git clone https://github.com/armgits/justbot.git justbot_project
sudo rm -rf ~/cakin_ws/src/justbot_project/CADFiles/ ~/cakin_ws/src/justbot_project/Code/ ~/cakin_ws/src/justbot_project/DockerFiles/
sudo chmod +x ~/catkin_ws/src/justbot_project/justbot/src/move.py
sudo chmod +x ~/catkin_ws/src/justbot_project/justbot/src/start.py

cd ~/catkin_ws
catkin_make clean && catkin_make
source ~/catkin_ws/devel/setup.bash
