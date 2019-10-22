#!/usr/bin/env python
import sys
import rospy
import subprocess
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from gotogoal import *
from ros_controller.srv import *

kaas = ""

def callback(data):
	for x in data.buttons:
		if data.buttons[3] == 1:
			print("Success")
			subprocess.call("python /home/rosw/catkin_ws/src/ros_controller/scripts/locatioinlogger.py 1", shell=True)
			#rospy.logwarn("Success", 1)
		if data.buttons[7] == 1:
			print("Success")
			subprocess.call("python /home/rosw/catkin_ws/src/ros_controller/src/gotogoal.py 1", shell=True)
			#rospy.logwarn("Success", 1)
		if data.buttons[2] == 1:
			rospy.wait_for_service('write_service')
			try:
				print("Success X pressed")
				print(kaas)
				global kaas
				write_file(kaas)
			   	write_service = rospy.ServiceProxy('write_service', WriteFile)
				resp1 = write_service(kaas)
				return resp1
			except rospy.ServiceException, e:
				print("Service call failed: %s", e)

def chatterCallback(data):
	print(data)
	global kaas
	kaas = data.data

def write_file(data):
	f = open("/home/rosw/catkin_ws/src/ros_controller/src/safeLocation.txt", "w")
	f.write(data)
	f.close()
		
def start():
        # publishing to "turtle1/cmd_vel" to control turtle1
        global pub
        pub = rospy.Publisher('rosaria/cmd_vel', Twist, queue_size=10)
        # subscribed to joystick inputs on topic "joy"
        rospy.Subscriber("joy", Joy, callback)
	rospy.Subscriber("/chatter", String, chatterCallback)
        # starts the node
        rospy.init_node('Joy2Turtle')
        rospy.spin()

if __name__ == '__main__':
     start()
