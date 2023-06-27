#!/bin/bash

cd ~/catkin_ws
source devel/setup.bash

roscore &
sleep 3
roslaunch justbot justbot_gazebo.launch &
sleep 3
rosrun justbot move.py &

wait -n
exit $?