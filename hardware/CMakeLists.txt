cmake_minimum_required(VERSION 3.17)                            
PROJECT(jh3)

SET(CMAKE_CXX_STANDARD 17)

FIND_PACKAGE( OpenCV REQUIRED ) 
FIND_PACKAGE( CURL REQUIRED )                             
INCLUDE_DIRECTORIES( ${OpenCV_INCLUDE_DIRS} )
INCLUDE_DIRECTORIES( ${CURL_INCLUDE_DIR} )

SET(SOURCE_FILES
	wrapper.cpp
	
	libs/robot_libs.h
	#libs/camera_module/my_object.h
	#libs/camera_module/stereo_cam.h
	#libs/camera_module/stereo_cam_helper.h
	
	libs/robot_module/robot.h
	libs/robot_module/robot_old.h
	
	libs/robot_motion_module/robot_motion.h
	libs/robot_motion_module/robot_motion_helper.h
)

ADD_EXECUTABLE(wrapper ${SOURCE_FILES})
TARGET_LINK_LIBRARIES (wrapper ${OpenCV_LIBS})
TARGET_LINK_LIBRARIES (wrapper ${CURL_LIBRARIES})
