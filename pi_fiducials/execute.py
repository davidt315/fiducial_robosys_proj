#!/usr/bin/python3
import numpy as np
import cv2
import picamera
import picamera.array
import logging
from state_machine import Robot

# Setup fiducial dictionary and params
DICTIONARY = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50) # our marker dictionary
tag = np.zeros((300, 300, 1), dtype="uint8")
cv2.aruco.drawMarker(DICTIONARY, 10, 300, tag, 1)
cv2.imwrite("images/test_tag.png", tag)
PARAMETERS = cv2.aruco.DetectorParameters_create() # default params

# picamera params
RESOLUTION = (1008,1008)
FRAMERATE = 30

def find_markers(frame):
	gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray_frame, DICTIONARY, parameters=PARAMETERS)

	result = set()
	if ids is None:
		# vid.write(frame)
		return result

	ids = ids.flatten()
	for (markerCorner, markerID) in zip(corners, ids):
		# extract the marker corners
		corners = markerCorner.reshape((4, 2))
		(topLeft, topRight, bottomRight, bottomLeft) = corners

		# convert each of the (x, y)-coordinate pairs to integers
		topRight = (int(topRight[0]), int(topRight[1]))
		bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
		bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
		topLeft = (int(topLeft[0]), int(topLeft[1]))
		# center coords
		x_cent = int((topLeft[0] + bottomRight[0])/2.0)
		y_cent = int((topLeft[1] + bottomRight[1])/2.0)
		width = abs(topRight[0] - bottomLeft[0])

		# annotate the frame
		# draw the bounding box of the ArUCo detection
		cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
		cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
		cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
		cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)
		cv2.circle(frame, (x_cent, y_cent), 4, (0, 0, 255), -1)
		# draw the ArUco marker ID on the frame
		cv2.putText(frame, str(markerID), (topLeft[0], topLeft[1] - 15),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

		# add result
		result.add((id, x_cent, y_cent, width))
	# write frame to vid
	# vid.write(frame)
	return result


def execute():
	# create the camera
	camera = picamera.PiCamera()
	camera.resolution = RESOLUTION # (1008,1008)
	camera.framerate = FRAMERATE # 30

	# create VideoWriter object
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	vid = cv2.VideoWriter('images/output.avi',fourcc, 20.0, RESOLUTION)

	# create the Robot
	car = Robot()

	rawCapture = picamera.array.PiRGBArray(camera, size=RESOLUTION)
	try:
		for capture in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
			frame = capture.array
			markers = find_markers(frame)
			
			car.act(markers)
			# print(markers)
			rawCapture.truncate(0)

	except KeyboardInterrupt:
		logging.exception("Keyboard interruption: exiting.")
	finally:
		camera.close()
		vid.release()


execute()
