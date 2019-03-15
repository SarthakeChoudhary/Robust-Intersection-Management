#!/usr/bin/env python
import rospy
import std_msgs.msg
import math

flag = 0

def callback(msg):
    global flag
    print(msg)
    if(msg == std_msgs.msg.Int8(64)):
        print('hello')
        flag = 1

if __name__ == '__main__':
    global flag
    rospy.init_node('IM')
    pub = rospy.Publisher('/comm', std_msgs.msg.Int8,queue_size=1)
    sub = rospy.Subscriber('/comm', std_msgs.msg.Int8, callback)
    while not rospy.is_shutdown():
        if flag == 1:
            pub.publish(2)
    rospy.spin()