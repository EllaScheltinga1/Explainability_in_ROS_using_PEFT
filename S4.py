#!/usr/bin/env python

import rospy
import os
import subprocess
from std_srvs.srv import Empty # type: ignore
from geometry_msgs.msg import PoseWithCovarianceStamped  # type: ignore
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal # type: ignore
import actionlib # type: ignore
import signal

# For Scenario 2 Camera
from gazebo_msgs.srv import SpawnModel, SpawnModelRequest # type: ignore
from geometry_msgs.msg import Pose # type: ignore
import numpy as np
from sensor_msgs.msg import Image # type: ignore
from cv_bridge import CvBridge, CvBridgeError # type: ignore
import cv2

# Global flag to indicate if the robot is near the obstacle
near_obstacle = False


def start_rosbag_recording():
    # Start rosbag recording
    rosbag_process = subprocess.Popen(['rosbag', 'record', '/rosout', '-O', 'S4W1_3.bag'])
    return rosbag_process

def stop_rosbag_recording(rosbag_process):
    # Stop rosbag recording
    rosbag_process.terminate()
    rosbag_process.wait()

def call_service(service_name):
    rospy.wait_for_service(service_name)
    try:
        service = rospy.ServiceProxy(service_name, Empty)
        service()
        rospy.loginfo(f"Service call to {service_name} succeeded.")
    except rospy.ServiceException as e:
        rospy.logerr(f"Service call to {service_name} failed: {e}")

def set_waypoints():
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    rospy.loginfo("Waiting for move_base action server...")
    client.wait_for_server()
    rospy.loginfo("Connected to move_base action server.")

    # Define waypoints and navigate
    waypoints = [
        {'x': 3.0, 'y': 1.0, 'w': 1.0, 'seq': 1},
        # {'x': 3.0, 'y': -7.0, 'w': 1.0, 'seq': 2},
        # {'x': -2.0, 'y': -12.0, 'w': 1.0, 'seq': 3},
        # {'x': 3.0, 'y': 0.0, 'w': 1.0, 'seq': 4},
        # {'x': 3.0, 'y': 1.0, 'w': 1.0, 'seq': 5} 
    ]

    for waypoint in waypoints:
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = waypoint['x']
        goal.target_pose.pose.position.y = waypoint['y']
        goal.target_pose.pose.orientation.w = waypoint['w']
        goal.target_pose.header.seq = waypoint['seq']

        rospy.loginfo(f"Sending goal {waypoint['seq']} to move_base: x={waypoint['x']}, y={waypoint['y']}")
        client.send_goal(goal)
        rospy.loginfo(f"Navigating to waypoint {waypoint['seq']}...")
        # client.wait_for_result()

        # Wait for result with a timeout of 30 seconds
        finished_within_time = client.wait_for_result(rospy.Duration(30))

        if client.get_state() == actionlib.GoalStatus.SUCCEEDED and finished_within_time:
            rospy.loginfo(f"Reached waypoint {waypoint['seq']}")
        else:
            rospy.logwarn(f"Failed to reach waypoint {waypoint['seq']}")

def spawn_obstacle():
    # Wait for the spawn_model service
    rospy.wait_for_service('/gazebo/spawn_sdf_model')
    try:
        # Read the obstacle model file
        model_path = "../Desktop/Thesis/obstacle.sdf"
        with open(model_path, 'r') as model_file:
            model_xml = model_file.read()

        # Define the initial pose of the obstacle
        initial_pose = Pose()
        initial_pose.position.x = 2.5
        initial_pose.position.y = 0.0
        initial_pose.position.z = 0.0
        initial_pose.orientation.w = 1.0

        # Call the service to spawn the model
        spawn_model_prox = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
        req = SpawnModelRequest()
        req.model_name = "obstacle"
        req.model_xml = model_xml
        req.initial_pose = initial_pose
        req.reference_frame = "world"

        spawn_model_prox(req)
        rospy.loginfo("Obstacle spawned in Gazebo.")
        return initial_pose.position  # Return the position of the obstacle
    except rospy.ServiceException as e:
        rospy.logerr(f"Failed to spawn obstacle: {e}")
        return None


class RedCubeDetector:
    def __init__(self, obstacle_position):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/xtion/rgb/image_raw", Image, self.image_callback)
        self.red_cube_detected = False
        self.obstacle_position = obstacle_position  # Store the obstacle position
        self.current_position_sub = rospy.Subscriber("/amcl_pose", PoseWithCovarianceStamped, self.update_current_position)
        self.current_position = None

    def update_current_position(self, data):
        self.current_position = data.pose.pose.position
        
    def image_callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(f"CvBridge Error: {e}")
            return

        # Convert BGR image to HSV
        hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

        # Define the red color range in HSV (including darker shades)
        lower_red1 = np.array([0, 50, 50])
        upper_red1 = np.array([10, 255, 255])
        mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)

        lower_red2 = np.array([170, 50, 50])
        upper_red2 = np.array([180, 255, 255])
        mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)

        # Combine the masks to get the final mask
        red_mask = mask1 + mask2

        # Apply morphological operations to enhance the mask
        kernel = np.ones((5, 5), np.uint8)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)

        # Find contours in the mask
        contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # print("This is the contour:", contours)
        if contours:
            # Find the largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)

            # Check if the detected contour is above a certain area threshold to avoid noise
            if area > 100:
                x, y, w, h = cv2.boundingRect(largest_contour)
                cv2.rectangle(cv_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                if not self.red_cube_detected:
                    rospy.loginfo(f"New obstacle detected at position ({self.obstacle_position.x}, {self.obstacle_position.y})")
                    self.red_cube_detected = True
            else:
                self.red_cube_detected = False
        else:
            self.red_cube_detected = False

        # Display the image with detection (for debugging purposes)
        cv2.imshow("Red Cube Detection", cv_image)
        cv2.waitKey(1)

        # Check if the robot is within 3 meters of the obstacle
        if self.current_position:
            distance = np.sqrt((self.current_position.x - self.obstacle_position.x)**2 +
                               (self.current_position.y - self.obstacle_position.y)**2)
            if distance <= 2.5:
                rospy.loginfo("Robot is nearing the obstacle. Path is being replanned.")
                rospy.sleep(10)
                near_obstacle = True
            else:
                near_obstacle = False


def cleanup_processes(rosbag_process, gazebo_process):
    # Stop recording rosbag
    stop_rosbag_recording(rosbag_process)
    rospy.loginfo("Rosbag recording stopped.")
    
    # Terminate Gazebo process
    gazebo_process.terminate()
    gazebo_process.wait()
    rospy.loginfo("Gazebo process stopped.")

def main():
    rospy.init_node('tiago_autonomous_navigation', log_level=rospy.DEBUG)

    # Set the environment variable LIBGL_ALWAYS_SOFTWARE
    os.environ['LIBGL_ALWAYS_SOFTWARE'] = '1'

    # Start the Gazebo simulation with the Tiago robot
    gazebo_process = subprocess.Popen(['roslaunch', 'tiago_2dnav_gazebo', 'tiago_navigation.launch', 'public_sim:=true', 'lost:=false']) # , 'world:=pal_office'

    # Allow some time for Gazebo to fully start
    rospy.sleep(10)

    print("Starting to spawn obstacle")
    # Spawn the obstacle in Gazebo
    obstacle_position = spawn_obstacle()

    # Start recording rosbag
    rosbag_process = start_rosbag_recording()

    # Initialize red cube detector
    detector = RedCubeDetector(obstacle_position)

    try:
        rospy.sleep(5)

        # Set waypoints for autonomous navigation
        set_waypoints()

    finally:
        # Cleanup processes
        cleanup_processes(rosbag_process, gazebo_process)

if __name__ == "__main__":
    main()
