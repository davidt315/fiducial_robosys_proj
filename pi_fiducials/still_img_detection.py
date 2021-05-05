#!/usr/bin/python3
#################################################################################################
# This Segment was used to test a still image detection
################################################################################################# 
import numpy as np
import cv2
import picamera
import picamera.array

# Setup fiducial dictionary and params
DICTIONARY = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250) # our marker dictionary
tag = np.zeros((300, 300, 1), dtype="uint8")
cv2.aruco.drawMarker(DICTIONARY, 10, 300, tag, 1)
cv2.imwrite("images/still_test_tag.png", tag)
PARAMETERS = cv2.aruco.DetectorParameters_create() # default params
MARKER_EDGE = 0.05 # not really relevant for our use case; our marker size is 5cm x 5cm

# picamera params
RESOLUTION = (1008,1008)
FRAMERATE = 30


image = cv2.imread("testing_image.jpg")
(corners, ids, rejected) = cv2.aruco.detectMarkers(image, DICTIONARY, parameters=PARAMETERS)
if len(corners) > 0:
	# flatten the ArUco IDs list
	ids = ids.flatten()
	# loop over the detected ArUCo corners
	for (markerCorner, markerID) in zip(corners, ids):
		# extract the marker corners (which are always returned in
		# top-left, top-right, bottom-right, and bottom-left order)
		corners = markerCorner.reshape((4, 2))
		(topLeft, topRight, bottomRight, bottomLeft) = corners
		# convert each of the (x, y)-coordinate pairs to integers
		topRight = (int(topRight[0]), int(topRight[1]))
		bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
		bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
		topLeft = (int(topLeft[0]), int(topLeft[1]))

        # draw the bounding box of the ArUCo detection
		cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
		cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
		cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
		cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
		# compute and draw the center (x, y)-coordinates of the ArUco
		# marker
		cX = int((topLeft[0] + bottomRight[0]) / 2.0)
		cY = int((topLeft[1] + bottomRight[1]) / 2.0)
		cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
		# draw the ArUco marker ID on the image
		cv2.putText(image, str(markerID),
			(topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
			0.5, (0, 255, 0), 2)
		print("[INFO] ArUco marker ID: {}".format(markerID))
		# show the output image
		cv2.imwrite("output.jpg", image)
		cv2.waitKey(0)