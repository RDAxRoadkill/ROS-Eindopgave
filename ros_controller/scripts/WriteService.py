#!/usr/bin/env python

from ros_controller.srv import WriteFile, WriteFileResponse
#,AddTwoIntsResponse
import rospy

#def handle_add_two_ints(req):
#    print "Returning [%s + %s = %s]"%(req.a, req.b, (req.a + req.b))
#    return AddTwoIntsResponse(req.a + req.b)

def handle_write(data):
    print "Kaas geschreven"
    print str(data.a)
    write_file(str(data.a))

def write_server():
    rospy.init_node('write_service_server')
    s = rospy.Service('write_service', WriteFile, handle_write)
    print "Ready to write"
    rospy.spin()
    return true

def write_file(data):
	f = open("/home/rosw/catkin_ws/src/ros_controller/src/safeLocation.txt", "w")
	f.write(data)
	f.close()

if __name__ == "__main__":
    write_server()
