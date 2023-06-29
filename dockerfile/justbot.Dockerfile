FROM ubuntu:focal

ENV DEBIAN_FRONTEND=noninteractive

# setup timezone
RUN echo 'Etc/UTC' > /etc/timezone && \
    ln -s /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    apt-get update && \
    apt-get install -q -y --no-install-recommends tzdata && \
    rm -rf /var/lib/apt/lists/*

# install packages
RUN apt-get update && apt-get install -q -y --no-install-recommends \
    dirmngr \
    gnupg2 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# setup sources.list
RUN echo "deb http://packages.ros.org/ros/ubuntu focal main" > /etc/apt/sources.list.d/ros1-latest.list

# setup keys
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

# setup environment
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

ENV ROS_DISTRO noetic

# noetic desktop installation
RUN apt update \
  && apt install -y --no-install-recommends ros-noetic-ros-base \
    python3-rosdep \
    python3-rosinstall \
    python3-wstool \
    build-essential \
    ros-noetic-gazebo-ros-pkgs \
    ros-noetic-gazebo-ros-control \
    ros-noetic-joint-state-controller \
    ros-noetic-effort-controllers \
    ros-noetic-xacro \
    ros-noetic-robot-state-publisher \
    ros-noetic-joint-state-publisher \
    git \
    python-is-python3 \
  && curl -sSL http://get.gazebosim.org | sh \
  && rosdep init \
  && rosdep update

# copy scripts for workspace creation and package installation
COPY justbot_setup.sh /
COPY justbot_execute.sh /
RUN chmod +x /justbot_setup.sh \
  && chmod +x /justbot_execute.sh

# add a non-root user
ARG USERNAME=noetic
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ENV ROS_DISTRO=noetic

RUN groupadd --gid $USER_GID $USERNAME \
  && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
  && apt-get update \
  && apt-get install -y sudo \
  && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
  && chmod 0440 /etc/sudoers.d/$USERNAME \
  && echo "if [ -f /opt/ros/${ROS_DISTRO}/setup.bash ]; then source /opt/ros/${ROS_DISTRO}/setup.bash; fi" >> /home/$USERNAME/.bashrc

# create catkin workspace and install the justbot packages using the scripts
USER $USERNAME

RUN mkdir -p /home/$USERNAME/catkin_ws/src && cd /home/$USERNAME/catkin_ws/ \
  && echo "if [ -f /home/$USERNAME/catkin_ws/devel/setup.bash ]; then source /home/$USERNAME/catkin_ws/devel/setup.bash; fi" >> /home/$USERNAME/.bashrc \
  && /justbot_setup.sh

ENV DEBIAN_FRONTEND=

ENTRYPOINT [ "/justbot_execute.sh" ]