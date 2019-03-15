#!/usr/bin/env python
import rospy
import math
import std_msgs.msg
from sensor_msgs.msg import LaserScan
import geometry_msgs.msg
from nav_msgs.msg import Odometry

vel= 0.2

def callback_im(msg):
    print(msg)
    global vel
    vel = int(msg)

def callback_odom(msg):
    # print(msg.pose.pose.position.x)
    if (msg.pose.pose.position.x >= -2):
        pub_im.publish(64)

def callback_laser(msg):
    # print((msg.ranges[354:366]))
    global vel
    for i in msg.ranges[356:365]:
        if (i < 0.5):
            vel = 0
            break


if __name__ == '__main__':

    rospy.init_node('Car_Controller')
    pub_car_vel = rospy.Publisher('/robot1/cmd_vel', geometry_msgs.msg.Twist, queue_size=1)
    pub_im = rospy.Publisher('/comm', std_msgs.msg.Int8, queue_size=1)
    # sub_im = rospy.Subscriber('/comm', std_msgs.msg.Int8, callback_im)
    sub_odom = rospy.Subscriber('/robot1/odom', Odometry, callback_odom)
    sub_laser = rospy.Subscriber('/mybot/laser/scan', LaserScan, callback_laser)
    cmd = geometry_msgs.msg.Twist()
    while not rospy.is_shutdown():
        cmd.linear.x = vel
        # print(cmd.linear.x)
        pub_car_vel.publish(cmd)

    rospy.spin()