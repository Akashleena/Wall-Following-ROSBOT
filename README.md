# Wall following bot

1. To launch the world
```
$roslaunch turtlebot3_gazebo turtlebot3_empty_world.launch 

```
2. Select rectangular_wall from the insert menu of Gazebo or if you cannot find it it's in catkin_ws/world/rectangular_wall

3. In a second terminal launch the wall_following_robot node using the command

```
$source devel/setup.bash
$roslaunch motion_plan laser.launch

```
_Demo Video_
[Link](https://drive.google.com/file/d/1scNui854kLw95vsSjZAF-IBm0Jt2OdZf/view?usp=sharing)
