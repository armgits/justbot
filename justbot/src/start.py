#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from math import pi

home_pos = [0, -1.5708, 1.5708, -1.5708, 1.5708, 0, -0.0174533]

rospy.init_node('set_home', anonymous=True)

j1_pub = rospy.Publisher('/justbot/joint_1_controller/command', Float64, queue_size=1)
j2_pub = rospy.Publisher('/justbot/joint_2_controller/command', Float64, queue_size=1)
j3_pub = rospy.Publisher('/justbot/joint_3_controller/command', Float64, queue_size=1)
j4_pub = rospy.Publisher('/justbot/joint_4_controller/command', Float64, queue_size=1)
j5_pub = rospy.Publisher('/justbot/joint_5_controller/command', Float64, queue_size=1)
j6_pub = rospy.Publisher('/justbot/joint_6_controller/command', Float64, queue_size=1)
tool_pub = rospy.Publisher('/justbot/tool_controller/command', Float64, queue_size=1)

def set_home():
    msg = Float64()
    #rospy.loginfo(msg)
    rate = rospy.Rate(5)
    counter = 0
    while counter < 10:
        msg.data = home_pos[0]
        j1_pub.publish(msg)
        msg.data = home_pos[1]
        j2_pub.publish(msg)
        msg.data = home_pos[2]
        j3_pub.publish(msg)
        msg.data = home_pos[3]
        j4_pub.publish(msg)
        msg.data = home_pos[4]
        j5_pub.publish(msg)
        msg.data = home_pos[5]
        j6_pub.publish(msg)
        msg.data = home_pos[6]
        tool_pub.publish(msg)
        #rospy.loginfo("Joint angles published")
        counter += 1
        rate.sleep()

if __name__ == '__main__':
    try:
        set_home()
        rospy.loginfo("Set")
    except rospy.ROSInterruptException:
        pass