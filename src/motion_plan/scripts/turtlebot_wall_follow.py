#! /usr/bin/env python

# import ros stuff
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf import transformations

import math

active_ = False
pub_ = None
regions_ = {
        'right': 0,
        'fright': 0,
        'front': 0,
        'fleft': 0,
        'left': 0,
}
regions=dict()
state_ = 0
state_dict_ = {

    0: 'find a wall',
    1: 'go straight',
    2: 'turn left',
    3: 'turn right',
    4: 'steer right and go straight',
    5: 'go straight and turn left',
    6: 'go back and turn right',
}

def clbk_laser(msg):
    global regions_
    print("Hello Ji! Myself inside Callback laser fcn!")
    regions_ = {
        'fleft': min(min(msg.ranges[0:71]), 10),
        'left': min(min(msg.ranges[72:143]), 10),
        'back': min(min(msg.ranges[144:215]), 10),
        'right': min(min(msg.ranges[216:287]), 10),
        'fright': min(min(msg.ranges[288:359]), 10),
    }
    
    take_action()


def take_action():
    global regions_
    regions = regions_
    msg = Twist()
    linear_x = 0
    angular_z = 0
    
    state_description = ''
    
    d = 0.5
    
    if regions['fright'] > d and regions['fleft'] > d and regions['right'] > d and regions['left'] > d and regions['back']> d:
        state_description = 'case 0 - Nothing detected, find a wall'
        print('case 0 - Nothing detected, find a wall')
        state_(0)
    if regions['fright'] < d and regions['fleft'] < d and regions['right'] > d and regions['left'] > d and regions['back']> d:
        state_description = 'case 1 - Wall only in front detected'
        print('case 1- Wall only in front detected')
        state_(3)
    elif regions['left'] < d and regions['fleft'] < d and regions['fright'] > d and regions['right'] > d and regions['back']>d:
        state_description = 'case 2 - wall on the left'
        print(state_description)
        state_(1)
        
    elif regions['fright'] < d and regions['fleft'] < d and regions['left'] < d and regions['right']> d and regions['back']> d:
        state_description = 'case 3 - wall on front and left'
        print(state_description)
        state_(3)
        
    elif regions['back'] < d and regions['left'] < d and regions['fright'] > d and regions['right'] > d or regions['fleft'] < d:
        state_description = 'case 4 - Wall on left and back'
        print(state_description)
        state_(5)
        
    #### the following condition did work well ####    
    elif regions['left'] < d and regions['back'] < d and regions['fright'] > d and regions['fleft']> d and regions['right'] > d:
        state_description = 'case 5 - wall only on left but we have reached the extreme end so we turn left'
        print(state_description)
        state_(2)
        
    elif regions['right'] < d and regions['left'] < d and regions['back'] < d:
        state_description = 'case 6 - go straight and steer a bit right because there is wall on 3 sides'
        print(state_description)
        state_(6)
        
    elif regions['fright'] < d and regions['right'] < d and regions['fleft'] > d and regions['left']> d and regions['back']> d:
        state_description = 'case 7 - walls on right and front'
        print('we turn right, this is case 7 walls on right and front')
        state_(3)
        
    elif regions['right'] < d and regions['fleft'] > d and regions['fright'] > d and regions['left'] > d and regions['back']> d:
        state_description = 'case 8 - walls only on right'
        print('case 8 - walls only on right : we turn right')
        state_(3)
        
    elif regions['right'] < d and regions['left'] < d  and regions['fright'] > d and regions['fleft'] >d and regions['back'] > d:
    	state_description= 'case 9- walls on right and left'
    	print('case 9- walls on right and left: so we go straight and turn left')
    	state_(5)
    	
    
    #elif regions['fright'] < d and regions['fleft'] < d and regions['right'] < d and regions['left'] <d and regions['back'] > d:
    	#state_description= 'case 10- Walls on front right and left'
    	#print('case 10- Walls on front right and left : so we go back and turn right')
    	#change_state(6)
      
    else:
        state_description = 'unknown case'
        print('Unknow case and we print the regions')
        rospy.loginfo(regions)

def find_wall():
    print('Inside find_wall function')   
    msg = Twist()
    msg.linear.x = 0.2
    msg.angular.z = -0.2
    return msg
    
def go_straight():
    print('Inside go straight function')
    msg = Twist()
    msg.linear.x = 0.2
    return msg

def turn_left():
    print('Inside turn left function')
    msg = Twist()
    msg.angular.z = 0.2
    return msg
    
def turn_right():
    print('Inside turn right function')
    msg = Twist()
    msg.angular.z = -0.2
    return msg

def steer_right_go_straight():
    print('Inside Steer right and go straight function')
    msg = Twist()
    msg.angular.z= 0.2
    msg.linear.x = 0.2
    return msg
    
def go_straight_turn_left():
    print('Inside go straight turn left function')
    msg = Twist()
    msg.angular.z= 0.3
    msg.linear.x = 0.2
    return msg
    
def go_back_turn_right():
    print('Inside go back turn right function')
    msg = Twist()
    msg.angular.z= -0.2
    msg.linear.x = -0.2
    return msg
    


def main():
    global pub_, active_
    
    rospy.init_node('wall_following_robot')
    
    pub_ = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    
    sub = rospy.Subscriber('/scan', LaserScan, clbk_laser)
    
    rate = rospy.Rate(2)
    print("Keep calm and debug Aleena")
    while not rospy.is_shutdown():
        msg = Twist()
        print("we are printing twist()")
        
        if state_ == 0:
            msg = find_wall()
        elif state_ == 1:
            msg = go_straight()
        elif state_ == 2:
            msg = turn_left()
        elif state_ == 3:
            msg = turn_right()
        elif state_ == 4:
            msg = steer_right_go_straight()
        elif state_ == 5:
            msg = go_straight_turn_left()
        elif state_ == 6:
            msg = go_back_turn_right()
            pass
        else:
            rospy.logerr('Unknown state!')
        
        pub_.publish(msg)
        
        rate.sleep()

if __name__ == '__main__':
    main()
