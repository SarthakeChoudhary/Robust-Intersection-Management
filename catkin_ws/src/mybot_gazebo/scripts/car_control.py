#!/usr/bin/env python
import rospy
import math
import std_msgs.msg
from sensor_msgs.msg import LaserScan
import geometry_msgs.msg
from nav_msgs.msg import Odometry

velocity= 0.2
position = 0
flag = 0
id = 1
emergency = 0
j = 0
rcv_im = [None] * 2

def send_data_to_IM():
    global emergency
    pub_im = rospy.Publisher('/comm2', std_msgs.msg.UInt8, queue_size=10)
    pub_im.publish(65)
    if emergency == 0:
        value = (128 + int(velocity*10))
        pub_im.publish(value)
        pub_im.publish(position)
    else:
        value = (192 + 3)       #11....11 control packet to indicate obstruction in path
        pub_im.publish(value)
        emergency = 2


def callback_im(msg):
    # print((msg.data))
    global velocity, rcv_im, j, flag
    if (j < 2):
        rcv_im[j] = msg.data
        j = j + 1

    if (j == 1 and rcv_im[0] >> 6 != 1):
        j=0
        if flag == 0:
            send_data_to_IM()

    if (j==2):
        packet_type = (rcv_im[1] >> 6)
        curr_id = rcv_im[0] & 63
        print(curr_id)
        print(packet_type)
        if (curr_id == id):
            if (packet_type == 2):
                velocity = (rcv_im[1] & 63)/ 10.0
                print('voa received', velocity)
                flag = 1                        #to indicate that voa has been received
            elif (packet_type >> 6 == 3):
                print('error')
        j=0



def callback_odom(msg):
    # print(msg.pose.pose.position.x)
    global flag, position
    position = msg.pose.pose.position.x
    if (position >= 2 and flag == 0):
        send_data_to_IM()

def callback_laser(msg):
    # print((msg.ranges[354:366]))
    global velocity, emergency
    for i in msg.ranges[350:370]:
        if (i < 1.5 and emergency != 2):
            emergency = 1
            send_data_to_IM()
            velocity = 0
            break


if __name__ == '__main__':

    rospy.init_node('Car_Controller')
    pub_car_vel = rospy.Publisher('/robot1/cmd_vel', geometry_msgs.msg.Twist, queue_size=1)
    pub_im = rospy.Publisher('/comm2', std_msgs.msg.UInt8, queue_size=10)
    sub_im = rospy.Subscriber('/comm1', std_msgs.msg.UInt8, callback_im)
    sub_odom = rospy.Subscriber('/robot1/odom', Odometry, callback_odom)
    sub_laser = rospy.Subscriber('/mybot/laser/scan', LaserScan, callback_laser)
    cmd = geometry_msgs.msg.Twist()
    while not rospy.is_shutdown():
        cmd.linear.x = velocity
        # print(cmd.linear.x)
        pub_car_vel.publish(cmd)

    rospy.spin()