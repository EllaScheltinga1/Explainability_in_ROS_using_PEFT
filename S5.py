#!/usr/bin/env python

import rospy
import os
import subprocess
from std_srvs.srv import Empty # type: ignore
from geometry_msgs.msg import PoseStamped # type: ignore
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal # type: ignore
from geometry_msgs.msg import PoseWithCovarianceStamped # type: ignore
import actionlib # type: ignore
import signal


def start_rosbag_recording():
    # Start rosbag recording
    rosbag_process = subprocess.Popen(['rosbag', 'record', '/rosout', '-O', 'S5W4_1.bag'])
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

def initialize_localization():
    # Call the /global_localization service
    call_service('/global_localization')

    # Optionally, sleep for a few seconds to let the localization process stabilize
    rospy.sleep(10)

    # Clear the costmaps
    call_service('/move_base/clear_costmaps')


def set_waypoints():
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    rospy.loginfo("Waiting for move_base action server...")
    client.wait_for_server()
    rospy.loginfo("Connected to move_base action server.")

    # Define waypoints and navigate
    waypoints = [
        {'x': 6.0, 'y': -14.5, 'w': 1.0, 'seq': 1},
        {'x': 1.5, 'y': -3.0, 'w': 1.0, 'seq': 2},
        {'x': -7.5, 'y': -6.0, 'w': 1.0, 'seq': 3},
        {'x': 3.0, 'y': -8.0, 'w': 1.0, 'seq': 4},
        # {'x': -3.0, 'y': -9.0, 'w': 1.0, 'seq': 5} 
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
        client.wait_for_result()
        
        if client.get_state() == actionlib.GoalStatus.SUCCEEDED:
            rospy.loginfo(f"Reached waypoint {waypoint['seq']}")
        else:
            rospy.logwarn(f"Failed to reach waypoint {waypoint['seq']}")


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
    rospy.sleep(20)

    # Start recording rosbag
    rosbag_process = start_rosbag_recording()  

    try:
        # Initialize localization
        # initialize_localization()
        rospy.sleep(5)
        # Set waypoints for autonomous navigation
        set_waypoints()

    finally:
        # Cleanup processes
        cleanup_processes(rosbag_process, gazebo_process)

if __name__ == "__main__":
    main()
