#!/usr/bin/env python
import rospy
import std_msgs.msg
import math

flag = 0
id = [0] * 64           #list of all the IDs
check = 0
j = 0
rcv_car = [None] * 3
velocity = [None] * 64
position = [None] * 64
curr_id= 70           #random value greater than 64
voa = [None] *64
voa[1] = 1
id[1] = 1
emergency = False

def send_data_to_car():

    if emergency == False:
        pub = rospy.Publisher('/comm1', std_msgs.msg.UInt8, queue_size=10)
        pub.publish(65)
        pub.publish(128 + (voa[curr_id] * 10.0))

    else:
        pub = rospy.Publisher('/comm2', std_msgs.msg.UInt8, queue_size=10)
        pub.publish(66)
        pub.publish(128 + (voa[curr_id] * 10.0))


def callback(msg):
    global flag, check, rcv_car,curr_id, emergency
    global j
    i = 3

    if j < i:
        rcv_car[j] = msg.data
        j = j + 1
    if j == 1 and rcv_car[0] >> 6 != 1:
        j = 0

    if j == 2:
        packet_type = rcv_car[1] >> 6
        if packet_type == 3:
             i = 2

    if j == i:
        packet_type = rcv_car[1] >> 6
        curr_id = (rcv_car[0] & 63)
        if (id[curr_id] == 1):
            if(packet_type == 2):
                velocity[curr_id] = (rcv_car[1] & 63)/10.0
                position[curr_id] = rcv_car[2]
                print("V-info received from car")
                print('velocity = ', velocity[curr_id])
                print('Position = ', position[curr_id])
                send_data_to_car()
            elif (packet_type == 3):
                value = rcv_car[1] & 63
                if(value == 3):
                    print('Emergency Detected \nRescheduling')
                    emergency = True
                    send_data_to_car()

        j=0


if __name__ == '__main__':
    rospy.init_node('IM')
    sub = rospy.Subscriber('/comm2', std_msgs.msg.UInt8, callback)
    rospy.spin()