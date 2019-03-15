#!/usr/bin/env python
import roslib
roslib.load_manifest('learning_tf')

import rospy
import tf

def shut():
    print("shutdown time")

def main():
    rospy.init_node("fixed_tf_broadcaster")
    br = tf.TransformBroadcaster()
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        br.sendTransform((0.0, 2.0, 0.0),
                         (0.0, 0.0, 0.0, 1.0),
                         rospy.Time.now(),
                         "carrot1",
                         "turtle1")
        rate.sleep()

if __name__ == '__main__':
    main()
    rospy.on_shutdown(shut())