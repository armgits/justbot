# Justbot
Justbot is 7 degrees of freedom (6 DOF arm and 1 DOF tool) articulated manipulator designed based on the DH parameters of the [UR5e Cobot from Universal Robots](https://www.universal-robots.com/products/ur5-robot/). This was my final project for the [ENPM662 (Introduction to Robot Modeling)](https://app.testudo.umd.edu/soc/search?courseId=ENPM662&sectionId=&termId=202308&_openSectionsOnly=on&creditCompare=&credits=&courseLevelFilter=ALL&instructor=&_facetoface=on&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on) course in the Fall 2022 semester.

## Description of contents
`CADFiles/` consists the Solidworks part and assembly files of the robot and tool plus Blender files of the same to export in DAE file format for the meshes.

`Code/` consists a Python file and Jupyter Notebooks for calculating forward kinematics and the Jacobian for inverse kinematics.

`DockerFiles/` consists the necessary files to build the Docker image of this project. The image can then be used to run the container as an executable for simulating in Gazebo. Building the Docker image locally is not recommended, an up-to-date image is available on the Dockerhub.

`justbot/` and `justool/` are the ROS packages for the arm and tool respectively. Justbot package has the `move.py` file which is the Python node that computes the inverse kinematics and publishes the joint values.

## Running the project
This project can only run on Linux at the moment. in the two following ways:
### In Docker container (Recommended)
This requires Docker (Linux) installation on your machine. If not, refer the [documentation](https://docs.docker.com/engine/install/)

Pull the Docker image of this project from Dockerhub
```
docker pull armdocks/justbot
```

Run the container for running the Gazebo simulation.
```
docker run -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix armdocks/justbot
```
>Tip: The -it argument can be omitted from the above command for a less verbose, clean terminal output.

### On local machine
This requires Ubuntu Focal (20.04) with ROS Noetic full desktop installation. Additional ROS packages that might be required are [joint state](http://wiki.ros.org/joint_state_controller) and [effort](http://wiki.ros.org/effort_controllers) controller packages and the [PyYAML](https://pypi.org/project/PyYAML/) Python package.

These additional packages can be installed by:

Joint state controllers package
```
apt install ros-noetic-joint-state-controller
```
Effort controllers package
```
apt install ros-noetic-effort-controllers
```
PyYAML package
```
pip3 install pyyaml
```
Assuming you have the catkin workspace setup, 

Clone the repository to `src/` folder of the target catkin workpace. Assuming this would be `~/catkin_ws/src/`,
```
git clone https://github.com/armgits/justbot.git ~/catkin_ws/src/justbot_project
```
Make the Python files `start.py` and `move.py` in the `src/` folder of justbot package executable.
```
sudo chmod +x ~/catkin_ws/src/justbot_project/justbot/src/move.py
sudo chmod +x ~/catkin_ws/src/justbot_project/justbot/src/start.py
```
Now you can build and source the packages.

After a successful build, run the simulation in Gazebo. 

This can be done in a single line using the shell script `justbot_execute.sh` from `DockerFiles/` folder.
```
~/catkin_ws/src/justbot_project/DockerFiles/justbot_execute.sh
```

Or manually,

In first terminal run `roscore` to initialize the ROS master.
```
roscore
```
In a new, second terminal run to spawn the robot in Gazebo.
```
roslaunch justbot justbot_gazebo.launch
```
In a new, third terminal run to run the node to perform the task.
```
rosrun justbot move.py
```

