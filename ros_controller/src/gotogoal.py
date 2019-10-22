#!/usr/bin/env python
#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt
from std_msgs.msg import String

def read_file():
	f = open("/home/rosw/catkin_ws/src/ros_controller/src/safeLocation.txt", "r")
	data = f.readline()
	f.close()
	return data

class TurtleBot:

    def __init__(self):
        # Creates a node with name 'turtlebot_controller' and make sure it is a
        # unique node (using anonymous=True).
        rospy.init_node('turtlebot_controller', anonymous=True)

        # Publisher which will publish to the topic '/turtle1/cmd_vel'.
        self.velocity_publisher = rospy.Publisher('rosaria/cmd_vel',Twist, queue_size=10000)

        # A subscriber to the topic '/turtle1/pose'. self.update_pose is called
        # when a message of type Pose is received.
        self.pose_subscriber = rospy.Subscriber('chatter', String, self.update_pose)

        self.pose = Pose()
        self.rate = rospy.Rate(100)


    def update_pose(self, data):
        """Current Position of the robot."""
	x = data.data.split(" ")
	self.pose.x = float(x[0])
	self.pose.y = float(x[1])

	rospy.loginfo(rospy.get_caller_id() + "LANG: " + str(self.pose.x))
	rospy.loginfo(rospy.get_caller_id() + "LONG: " + str(self.pose.y))

	

    def euclidean_distance(self, goal_pose):
        """Euclidean distance between current pose and the goal."""
        return sqrt(pow((goal_pose.x - self.pose.x), 6) +
                    pow((goal_pose.y - self.pose.y), 6))

    def linear_vel(self, goal_pose, constant=1.5):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
        return constant * self.euclidean_distance(goal_pose)

    def steering_angle(self, goal_pose):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
        return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)

    def angular_vel(self, goal_pose, constant=6):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
        return constant * (self.steering_angle(goal_pose) - self.pose.theta)

    def move2goal(self):
        """Moves the turtle to the goal."""
        goal_pose = Pose()

        # Get the input from the user.
	print(read_file())
	x = read_file()
	x = x.split(" ")
        goal_pose.x = float(x[0])
        goal_pose.y = float(x[1])
	rospy.loginfo(rospy.get_caller_id() + "LANG_GOAL: " + str(goal_pose.x))
	rospy.loginfo(rospy.get_caller_id() + "LONG_GOAL: " + str(goal_pose.y))

        # Please, insert a number slightly greater than 0 (e.g. 0.01).
        distance_tolerance = 1

        vel_msg = Twist()

        while self.euclidean_distance(goal_pose) >= distance_tolerance:
	    #print("Moving to goal")
            # Porportional controller.
            # https://en.wikipedia.org/wiki/Proportional_control

#x = R * cos(lat) * cos(lon)
#y = R * cos(lat) * sin(lon)
#z = R *sin(lat)
# R = approximate radius of earth (e.g. 6371KM).
	    
            # Linear velocity in the x-axis.
            vel_msg.linear.x = self.linear_vel(goal_pose)
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0

            # Angular velocity in the z-axis.
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = self.angular_vel(goal_pose)

            # Publishing our vel_msg
            self.velocity_publisher.publish(vel_msg)

            # Publish at the desired rate.
            self.rate.sleep()

        # Stopping our robot after the movement is over.
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)

        # If we press control + C, the node will stop.
        rospy.spin()

if __name__ == '__main__':
    try:
        x = TurtleBot()
        x.move2goal()
    except rospy.ROSInterruptException:
        pass

