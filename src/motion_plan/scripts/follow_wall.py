#! /usr/bin/env python


import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf import transformations
from std_srvs.srv import *

import math 
active_ = False
pub=None
regions1={'right': 0, 'fright': 0, 'front': 0, 'fleft': 0, 'left': 0,}
regions=dict()
state_= 0
state_dict= {
    0: 'find the wall',
    1: 'turn left',
    2: 'follow the wall',
}


def wall_follower_switch(req):
	global active_
	active_ = req.data
	res = SetBoolResponse()
	res.success = True
	res.message = 'Done!'
	return res

#To decide in which region the robot is lying based on laser values
def clbk_laser(msg): 
	print('Inside the callback laser')
	global regions1
    	# 360 / 5 = 72
	regions1 = {
        	min(min(msg.ranges[0:71]), 10),
        	min(min(msg.ranges[72:143]), 10),
        	min(min(msg.ranges[144:215]), 10),
        	min(min(msg.ranges[216:287]), 10),
        	min(min(msg.ranges[288:359]), 10),
	}
	rospy.loginfo(regions1)

	take_action()


def change_state(state):
	global state_, state_dict
	if state is not state_:
        	print ('Wall follower - [%s] - %s' % (state, state_dict[state]))
        	state_ = state

def take_action():
	global regions1
	regions = regions1
	msg = Twist()
	linear_x = 0
	angular_z = 0
    
	state_description = ''
	d=1.5
	print (d)
    	
	if regions['front'] > d and regions['fleft'] > d and regions['fright'] > d:
        	state_description = 'case 1- nothing'
        	print('case 1- nothing')
        	change_state(0)
	elif regions['front'] < d and regions['fleft'] > d and regions['fright'] > d:
        	state_description = 'case 2- front'
        	print('case 2- front')
        	change_state(1)
	elif regions['front'] > d and regions['fleft'] > d and regions['fright'] < d:
		state_description = 'case 3 - fright'
		print('case 3 - fright')
		change_state(2)
	elif regions['front'] > d and regions['fleft'] < d and regions['fright'] > d:
		state_description = 'case 4 - fleft'
		print('case 4 - fleft')
		change_state(0)
	elif regions['front'] < d and regions['fleft'] > d and regions['fright'] < d:
		state_description = 'case 5 - front and fright'
		print('case 5 - front and fright')
		change_state(1)
	elif regions['front'] < d and regions['fleft'] < d and regions['fright'] > d:
		state_description = 'case 6 - front and fleft'
		print('case 6 - front and fleft')
		change_state(1)
	elif regions['front'] < d and regions['fleft'] < d and regions['fright'] < d:
		state_description = 'case 7 - front and fleft and fright'
		print('case 7 - front and fleft and fright')
		change_state(1)
	elif regions['front'] > d and regions['fleft'] < d and regions['fright'] < d:
		state_description = 'case 8 - fleft and fright'
		print('case 8 - fleft and fright')
		change_state(0)
	else:
		state_description = 'unknown case'
		rospy.loginfo(regions)

def find_wall():
	print('Inside find_wall function')	
	msg = Twist()	
	msg.linear.x = 0.2
	msg.angular.z = -0.3
	return msg

def turn_left():
	print('Inside turn left function')
	msg = Twist()
	msg.angular.z = 0.3
	return msg

def follow_the_wall():
	print('Inside follow_the_wall function')
	global regions1
	msg = Twist()
	msg.linear.x = 0.2
	return msg

def main():
	global pub
	rospy.init_node('read_laser')
	pub= rospy.Publisher('/cmd_vel', Twist, queue_size=1)
	sub= rospy.Subscriber('scan',LaserScan, clbk_laser)  # queue size=1
	
	srv = rospy.Service('wall_follower_switch', SetBool, wall_follower_switch)
	rate = rospy.Rate(20)
	print('Inside main')
	while not rospy.is_shutdown():
		msg = Twist()
		if state_ == 0:
			msg = find_wall()
		elif state_ == 1:
			msg = turn_left()
		elif state_ == 2:
			msg = follow_the_wall()
		
		else:
			rospy.logerr('Unknown state!')
        
		pub.publish(msg)        
		rate.sleep()



if __name__ == '__main__':
	main()
    


