#!/usr/bin/env python

from ros_controller.srv import WriteFile, WriteFileResponse
import rospy

def handle_write(data):
    print str(data.a)
    write_file(str(data.a))
    return WriteFileResponse("Successfully wrote to file")

def write_server():
    rospy.init_node('write_service_server')
    #Define service name
    s = rospy.Service('write_service', WriteFile, handle_write)
    print "Ready to write"
    rospy.spin()

def write_file(data):
	f = open("/home/rosw/catkin_ws/src/ros_controller/src/safeLocation.txt", "w")
	f.write(data)
	f.close()

if __name__ == "__main__":
    write_server()
