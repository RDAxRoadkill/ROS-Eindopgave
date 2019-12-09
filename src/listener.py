#!/usr/bin/env python
import sys
import rospy
import subprocess
import math
import time
from std_msgs.msg import String
from geometry_msgs.msg import Point, Twist
from sensor_msgs.msg import Joy
from gotogoal import *
from ros_controller.srv import *


currentLocation = "5.0 5.0"
goal = "5.0 7.0"
newgoal = "6.0 7.0"

oldAngleToGoal = 0.0

buttonInX = False
buttonInY = False
buttonInStart = False
buttonInSelect = False

def callback(data):
	for x in data.buttons:
		if data.buttons[3] == 1 and buttonInY == False:
			buttonInY = True
			global buttonInY 

			print("Success Y pressed")	
			print("Goal location: " + goal)

			global goal
			write_file_goal(goal)

		if data.buttons[3] == 0:
			buttonInY = False
			global buttonInY

		if data.buttons[7] == 1 and buttonInStart == False:
			buttonInStart = True
			global buttonInStart

			print("Success StartButton")

			# Here we can use different attempts to turn robot
			goToAngle()

		if data.buttons[7] == 0:
			buttonInStart = False
			global buttonInStart
			
		if data.buttons[6] == 1 and buttonInSelect == False:
			buttonInSelect = True
			global buttonInSelect 
			print("Succes SelectPress")
			write_file("")
			write_file_goal("")
			print("Orientation reset")

		if data.buttons[6] == 0:
			buttonInSelect = False
			global buttonInSelect

		if data.buttons[2] == 1 and buttonInX == False:
			print("Success X pressed")
			buttonInX = True
			global buttonIn
			x = read_file()
	   		if x == "":
			    print("Location robot: " + currentLocation)
			    global currentLocation
			    write_file(currentLocation)
			else:
			    y = read_goal()
			    write_file(y)
			    print("Current location: " + y)
			    print("Goal location: " + newgoal)
		 	    global newgoal
			    write_file_goal(newgoal)
		if data.buttons[2] == 0:
			buttonInX = False
			global buttonInX
			


def chatterCallback(data):
	print(data)
	global currentLocation
	currentLocation = data.data

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

# Attempt 01 to turn robot
def goToAngle():
	#Using a constant turning rate, in a loop robot SHOULD turn

	#Keeping calculation exactly the same
	currentposX = 0.0
	currentposY = 0.0

	newGoalX = 40.0
	newGoalY = 25.0

	#Differences should be 40.0 & 25.0
	in_x = newGoalX - currentPosX
	in_y = newGoalY - currentPosY
	print("X difference: " + in_x + " Y difference: " +in_y)

	#Atan2 calc like old attempt
	angle_to_goal = atan2(in_y, in_x)
	#Calc new value for goal
	currentPos = atan2(currentposX, currentPosY)
	print("Angle to goal in radians: " + str(angle_to_goal))

	degree_to_goal = math.degrees(angle_to_goal)
	print("Angle to goal in degrees: " + str(degree_to_goal))

	while degree_to_goal != currentPos:
		print("Degree to goal: " + degree_to_goal)
		print("CurrentPos: " + currentPos)

		#TODO: Add right/Left logic here. currently just turning one way
		speed.linear.x = 1.0
		time.sleep(100)
		currentPos = currentPos + 1.0
		print("Updated currentPos" + currentPos)
		time.sleep(100)


# Attempt 00 to turn robot
def oldAttempt():
	currentposX = 0.0
	currentposY = 0.0

	y = read_file()
	print("Current location: " + y)
						
	y = y.split(" ")

    currentPosX = float(y[0])
    currentPosY = float(y[1])

	x = read_goal()
	print("Goal location: " + x)

	x = x.split(" ")
	#TODO: Fix error w/ floats
	newGoalX = float(x[0])
	newGoalY = float(x[1])

	in_x = newGoalX - currentPosX
	in_y = newGoalY - currentPosY

	angle_to_goal = atan2(in_y, in_x)
	print("Angle to goal in radians: " + str(angle_to_goal))

	degree_to_goal = math.degrees(angle_to_goal)
	print("Angle to goal in degrees: " + str(degree_to_goal))

	if degree_to_goal < 0:
		degree_to_goal = degree_to_goal * -1
		speed.linear.x = 2.0
		speed.angular.z = (-degree_to_goal*2)

	elif degree_to_goal > 0:
		degree_to_goal = degree_to_goal * 1
		speed.linear.x = 2.0
		speed.angular.z = (degree_to_goal*2)

	else:
		print("gedraaid")

		pub.publish(speed)
			
		time.sleep(2)
		speed.linear.x = 0.0
		speed.angular.z = 0.0	
		pub.publish(speed)		

def start():
    global pub
	global speed
    pub = rospy.Publisher('rosaria/cmd_vel', Twist, queue_size=10)
	#pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
	speed = Twist()
    # subscribed to joystick inputs on topic "joy"
    rospy.Subscriber("joy", Joy, callback)
	rospy.Subscriber("/chatter", String, chatterCallback)
    # starts the node
    rospy.init_node('Joy2Turtle')
    rospy.spin()

if __name__ == '__main__':
     start()
