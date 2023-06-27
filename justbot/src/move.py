#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
import math, numpy

rospy.init_node('line_follower', anonymous=True)

q1_pub = rospy.Publisher('/justbot/joint_1_controller/command', Float64, queue_size=1)
q2_pub = rospy.Publisher('/justbot/joint_2_controller/command', Float64, queue_size=1)
q3_pub = rospy.Publisher('/justbot/joint_3_controller/command', Float64, queue_size=1)
q4_pub = rospy.Publisher('/justbot/joint_4_controller/command', Float64, queue_size=1)
q5_pub = rospy.Publisher('/justbot/joint_5_controller/command', Float64, queue_size=1)
q6_pub = rospy.Publisher('/justbot/joint_6_controller/command', Float64, queue_size=1)
tool_pub = rospy.Publisher('/justbot/tool_controller/command', Float64, queue_size=1)

# Calculating Jacobian using the first method
def calc_jacobian(theta_1, theta_2, theta_3, theta_4, theta_5, theta_6, type):
    A1 = numpy.matrix([[round(math.cos(theta_1)), 0, round(math.sin(theta_1)), 0],
                [round(math.sin(theta_1)), 0, -round(math.cos(theta_1)), 0],
                [0, 1, 0, 0.1625],
                [0, 0, 0, 1]])

    A2 = numpy.matrix([[round(math.cos(theta_2)), -round(math.sin(theta_2)), 0, -0.425*round(math.cos(theta_2))],
                [round(math.sin(theta_2)), round(math.cos(theta_2)), 0, -0.425*round(math.sin(theta_2))],
                [0, 0, 1, 0],
                [0, 0, 0, 1]])

    A3 = numpy.matrix([[round(math.cos(theta_3)), -round(math.sin(theta_3)), 0, -0.3922*round(math.cos(theta_3))],
                [round(math.sin(theta_3)), round(math.cos(theta_3)), 0, -0.3922*round(math.sin(theta_3))],
                [0, 0, 1, 0],
                [0, 0, 0, 1]])
    
    A4 = numpy.matrix([[round(math.cos(theta_4)), 0, round(math.sin(theta_4)), 0],
                [round(math.sin(theta_4)), 0, -round(math.cos(theta_4)), 0],
                [0, 1, 0, 0.1333],
                [0, 0, 0, 1]])

    A5 = numpy.matrix([[round(math.cos(theta_5)), 0, -round(math.sin(theta_5)), 0],
                [round(math.sin(theta_5)), 0, round(math.cos(theta_5)), 0],
                [0, -1, 0, 0.0997],
                [0, 0, 0, 1]])

    A6 = numpy.matrix([[round(math.cos(theta_6)), -round(math.sin(theta_6)), 0, 0],
                [round(math.sin(theta_6)), round(math.cos(theta_6)), 0, 0],
                [0, 0, 1, 0.0996],
                [0, 0, 0, 1]])

    T1 = A1
    T2 = T1*A2
    T3 = T2*A3
    T4 = T3*A4
    T5 = T4*A5
    T6 = T5*A6

    O0 = numpy.array([ [0], [0], [0] ])
    O1 = numpy.array([ [T1[0, 3]], [T1[1, 3]], [T1[2, 3]] ])
    O2 = numpy.array([ [T2[0, 3]], [T2[1, 3]], [T2[2, 3]] ])
    O3 = numpy.array([ [T3[0, 3]], [T3[1, 3]], [T3[2, 3]] ])
    O4 = numpy.array([ [T4[0, 3]], [T4[1, 3]], [T4[2, 3]] ])
    O5 = numpy.array([ [T5[0, 3]], [T5[1, 3]], [T5[2, 3]] ])
    O6 = numpy.array([ [T6[0, 3]], [T6[1, 3]], [T6[2, 3]] ])

    Z0 = numpy.array([ [0], [0], [1] ])
    Z1 = numpy.array([ [T1[0, 2]], [T1[1, 2]], [T1[2, 2]] ])
    Z2 = numpy.array([ [T2[0, 2]], [T2[1, 2]], [T2[2, 2]] ])
    Z3 = numpy.array([ [T3[0, 2]], [T3[1, 2]], [T3[2, 2]] ])
    Z4 = numpy.array([ [T4[0, 2]], [T4[1, 2]], [T4[2, 2]] ])
    Z5 = numpy.array([ [T5[0, 2]], [T5[1, 2]], [T5[2, 2]] ])
    #Z6 = numpy.array([ [T6[0, 2]], [T6[1, 2]], [T6[2, 2]] ])

    J1 = numpy.concatenate((numpy.cross(Z0, numpy.subtract(O6, O0), axis=0), Z0), axis=0)
    J2 = numpy.concatenate((numpy.cross(Z1, numpy.subtract(O6, O1), axis=0), Z1), axis=0)
    J3 = numpy.concatenate((numpy.cross(Z2, numpy.subtract(O6, O2), axis=0), Z2), axis=0)
    J4 = numpy.concatenate((numpy.cross(Z3, numpy.subtract(O6, O3), axis=0), Z3), axis=0)
    J5 = numpy.concatenate((numpy.cross(Z4, numpy.subtract(O6, O4), axis=0), Z4), axis=0)
    J6 = numpy.concatenate((numpy.cross(Z5, numpy.subtract(O6, O5), axis=0), Z5), axis=0)

    J = numpy.concatenate((J1, J2, J3, J4, J5, J6), axis=1)
    
    if type == "inv":
        J_inv = numpy.linalg.pinv(J)
        return J_inv
    return J

q_arm = [0, -1.5708, 1.5708, -1.5708, 1.5708, -0.0174533]

def go(x_dist, y_dist, z_dist, time):
    loop_rate = 50
    waypoints = time*loop_rate
    rate = rospy.Rate(loop_rate)
    counter = 0
    while counter < time*loop_rate:
        Vx = -x_dist/time
        Vy = -y_dist/time
        Vz = z_dist/time
        X_dot = numpy.array([ [Vx], [Vy], [Vz], [0], [0], [0] ])

        q_dot = numpy.matmul(calc_jacobian(q_arm[0], q_arm[1], q_arm[2], q_arm[3], q_arm[4], q_arm[5], "inv"), X_dot)
        q_arm[0] = q_arm[0]+float(q_dot[0]*time/waypoints)
        q_arm[1] = q_arm[1]+float(q_dot[1]*time/waypoints)
        q_arm[2] = q_arm[2]+float(q_dot[2]*time/waypoints)
        q_arm[3] = q_arm[3]+float(q_dot[3]*time/waypoints)
        q_arm[4] = q_arm[4]+float(q_dot[4]*time/waypoints)
        q_arm[5] = q_arm[5]+float(q_dot[5]*time/waypoints)

        msg = Float64()
        msg.data = q_arm[0]
        q1_pub.publish(msg)
        msg.data = q_arm[1]
        q2_pub.publish(msg)
        msg.data = q_arm[2]
        q3_pub.publish(msg)
        msg.data = q_arm[3]
        q4_pub.publish(msg)
        # msg.data = q_arm[4]
        # q5_pub.publish(msg)
        # msg.data = q_arm[5]  # Fixing joints 5 and 6 since not required for this application
        # q6_pub.publish(msg)
        counter += 1
        rate.sleep()

def switch_tool():
    counter = 0
    while counter < 10:
        msg = Float64()
        msg.data = 1.5708
        tool_pub.publish(msg)
        counter +=1

if __name__ == '__main__':
    try:
        # Reaching the first screw
        go(-0.05, 0, 0, 1.5)
        go(-0.105, 0.20, -0.32, 1.5)
        rospy.loginfo("Unscrewing first screw")
        rospy.sleep(1)

        # Reaching the second screw
        go(0.052, 0, 0.15, 1.5)
        go(0.21, -0.06, -0.077, 1.5)
        rospy.loginfo("Unscrewing second screw")
        rospy.sleep(1)

        # Reaching the third screw
        go(-0.07, 0, 0.15, 1.5)
        go(0.093, -0.268, -0.187, 1.5)
        rospy.loginfo("Unscrewing third screw")
        rospy.sleep(1)

        # Reaching the fourth screw
        go(-0.1, 0, 0.15, 1.5)
        go(-0.19, -0.08, -0.21, 1.5)
        rospy.loginfo("Unscrewing fourth screw")
        rospy.sleep(1)

        # Reaching the center to pick the cover
        rospy.loginfo("Getting ready for pickup")
        go(0.05, 0, 0.15, 1.5)
        go(0, 0.2, 0, 1.5)
        rospy.sleep(1)

        # Switching tool to suction gripper
        switch_tool()
        rospy.loginfo("Ready to pickup")
        rospy.sleep(0.5)

        # Pick and place
        go(0, 0, -0.15, 1.5)
        rospy.sleep(0.5)
        go(0.07, 0, 0.35, 3)
        rospy.loginfo("Picked, ready to place")
        rospy.sleep(1)
        go(-0.6, 0.8, 0, 4)
        rospy.sleep(0.5)
        go(0, 0, -0.27, 2)
        rospy.loginfo("Placed")

    except rospy.ROSInterruptException:
        pass