#!/usr/bin/env python
#!/usr/bin/env python
import rospy
import subprocess
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from gotogoal import *

kaas = ""

def callback(data):
	for x in data.buttons:
		if data.buttons[7] == 1:
			print("Success")
			subprocess.call("python /home/rosw/catkin_ws/src/ros_controller/src/gotogoal.py 1", shell=True)
			#rospy.logwarn("Success", 1)
		if data.buttons[2] == 1:
			print("Success X pressed")
			global kaas
			write_file(kaas)
			print(kaas)

def chatterCallback(data):
	print(data)
	global kaas
	kaas = data.data
		
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

def write_file(data):
	f = open("/home/rosw/catkin_ws/src/ros_controller/src/safeLocation.txt", "w")
	f.write(data)
	f.close()

if __name__ == '__main__':
     start()
