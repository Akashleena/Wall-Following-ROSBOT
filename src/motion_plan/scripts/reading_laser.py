#! /usr/bin/env python

import rospy

from sensor_msgs.msg import LaserScan

def clbk_laser(msg):
    # 360 / 5 = 72
    regions = [
        min(min(msg.ranges[0:71]), 10),
        min(min(msg.ranges[72:143]), 10),
        min(min(msg.ranges[144:215]), 10),
        min(min(msg.ranges[216:287]), 10),
        min(min(msg.ranges[288:359]), 10),
    ]
    print("inside callback\n")
    print("at zero",msg.ranges[0])
    print("at 90",msg.ranges[90])
    print("at 180",msg.ranges[180])
    print("at 270",msg.ranges[270])
    print("at 359",msg.ranges[359])
    print (regions)
    
    rospy.loginfo(regions)

def main():
    rospy.init_node('reading_laser')
    
    sub = rospy.Subscriber('scan', LaserScan, clbk_laser)
    
    rospy.spin()

if __name__ == '__main__':
    main()

