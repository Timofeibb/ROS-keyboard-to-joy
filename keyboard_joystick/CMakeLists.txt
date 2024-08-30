cmake_minimum_required(VERSION 3.0.2)
project(keyboard_joystick)

## Find catkin and any catkin packages
find_package(catkin REQUIRED COMPONENTS
  rospy
  sensor_msgs
)

## Declare a catkin package
catkin_package()

## Specify additional locations of header files
include_directories(${catkin_INCLUDE_DIRS})

## Mark executables and/or libraries for installation
catkin_install_python(PROGRAMS
  scripts/keyboard_joystick.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)