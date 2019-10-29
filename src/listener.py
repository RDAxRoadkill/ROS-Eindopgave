#!/usr/bin/env python
import sys
import rospy
import subprocess
import math
from std_msgs.msg import String
from geometry_msgs.msg import Point, Twist
from sensor_msgs.msg import Joy
from turtlesim.msg import Pose
from gotogoal import *
from ros_controller.srv import *


kaas = ""
goal = ""

def callback(data):
	for x in data.buttons:
		if data.buttons[3] == 1:
			print("Success LocationLogger")
			#subprocess.call("python /home/rosw/catkin_ws/src/ros_controller/scripts/locatioinlogger.py 1", shell=True)
			#rospy.logwarn("Success", 1)
			print(goal)
			global goal
			write_file_goal(goal)
		if data.buttons[7] == 1:
			#subprocess.call("python /home/rosw/catkin_ws/src/ros_controller/src/gotogoal.py 1", shell=True)
			#rospy.logwarn("Success", 1)
			print("Success StartButton")
			currentposX = 0.0
			currentposY = 0.0
			y = read_goal()
	   		y = y.split(" ")

        		currentPosX = float(y[0])
        		currentPosY = float(y[1])
			print(currentPosX)
			print(currentPosY)
			#TODO: Get location & write to file, current is demo
			newGoalX = 51.383839
			newGoalY = 3.514512
			print(newGoalX)
			print(newGoalY)

			in_x = newGoalX - currentPosX
			in_y = newGoalY - currentPosY
			print(in_x)
			print(in_y)
			#Orientation
			angle_to_goal = atan2(in_y, in_x)
			print(angle_to_goal)
			#Change radials to degrees
			degree_to_goal = math.degrees(angle_to_goal)
			print(degree_to_goal)
			#Get old angle_to_goal
			oldAngleToGoal = -58.3924977503
			#if flip == True:
			#	new_angle_to_goal - selectAngle
			#	simAngle = selectAngle
			#	flip = false
			#else:
			#	simAngle = simAngle - 0.02
			#publisher
			#Start turning code
			if abs(angle_to_goal - oldAngleToGoal) > 0.1:
				#test in real lyf
				#speed = 0.3
				#0.02 = 1 degree turn
				oldAngleToGoal -= 0.3
				speed.linear.x = 0.0
				speed.angular.z = 0.3
			pub.publish(speed)
			#TODO: Make this repeatable theta is old 2nd
			
		if data.buttons[6] == 1:
			print("Succes SelectPress")
			print(flip)
			homeX = 0.0
			homeY = 0.0
			goalX = 0.0
			goalY = 0.0

			x = read_file()
	   		x = x.split(" ")

        		homeX = float(x[0])
        		homeY = float(x[1])

			y = read_goal()
	   		y = y.split(" ")

        		goalX = float(y[0])
        		goalY = float(y[1])

			print("HomeX: %s", homeX)
			print("HomeY: %s", homeY)

			print("GoalX: %s", goalX)
			print("GoalY: %s", goalY)
			inc_x = goalX - homeX
			inc_y = goalY - homeY
			print(inc_x)
			print(inc_y)
			#Orientation
			angle_to_goal = atan2(inc_y, inc_x)
			selectAngle = angle_to_goal
			flip = None
			print(angle_to_goal)
			#Change radials to degrees
			degree_to_goal = math.degrees(angle_to_goal)
			print(degree_to_goal)
		if data.buttons[2] == 1:
			print("Success X pressed")
			print(kaas)
			global kaas
			write_file(kaas)	
			#rospy.wait_for_service('write_service')
			#try:
			#	print("Success X pressed")
			#	print(kaas)
			#	global kaas
			#	write_file(kaas)
			#  	write_service = rospy.ServiceProxy('write_service', WriteFile)
			#	resp1 = write_service(kaas)
			#	return resp1
			#except rospy.ServiceException, e:
			#	print("Service call failed: %s", e)

def chatterCallback(data):
	print(data)
	global kaas
	kaas = data.data

def write_file(data):
	f = open("/home/rosw/catkin_ws/src/ros_controller/src/safeLocation.txt", "w")
	f.write(data)
	f.close()

def read_file():
	f = open("/home/rosw/catkin_ws/src/ros_controller/src/safeLocation.txt", "r")
	data = f.readline()
	f.close()
	return data

def write_file_goal(data):
	f = open("/home/rosw/catkin_ws/src/ros_controller/src/goal.txt", "w")
	f.write(data)
	f.close()

def read_goal():
	f = open("/home/rosw/catkin_ws/src/ros_controller/src/goal.txt", "r")
	data = f.readline()
	f.close()
	return data

def old_write_file_goal(data):
	f = open("/home/rosw/catkin_ws/src/ros_controller/src/oldGoal.txt", "w")
	f.write(data)
	f.close()

def old_read_goal():
	f = open("/home/rosw/catkin_ws/src/ros_controller/src/oldGoal.txt", "r")
	data = f.readline()
	f.close()
	return data
		
def start():
        # publishing to "turtle1/cmd_vel" to control turtle1
        global pub
	global speed
	global flip
	global selectAngle
	global simAngle
        #pub = rospy.Publisher('rosaria/cmd_vel', Twist, queue_size=10)
	pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
	speed = Twist()
        # subscribed to joystick inputs on topic "joy"
        rospy.Subscriber("joy", Joy, callback)
	rospy.Subscriber("/chatter", String, chatterCallback)
        # starts the node
        rospy.init_node('Joy2Turtle')
        rospy.spin()

if __name__ == '__main__':
     start()
