
#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
def clbk_laser(msg):
    print ('At zero',msg.ranges[0])
    rospy.loginfo("I heard laser at 360 %s", msg.ranges[90])

def main():

    rospy.init_node('read_laser')
    sub = rospy.Subscriber('scan',LaserScan, clbk_laser)  # queue size=1
    rospy.spin()

if __name__ == '__main__':
    main()
