#!/usr/bin/python3
import numpy as np
import cv2
import picamera
import picamera.array
import logging
import RPi.GPIO as io 
from state_machine import Robot

class RunCar():
	def __init__(self):
		# Setup fiducial dictionary and params
		self.DICTIONARY = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50) # our marker dictionary
		self.PARAMETERS = cv2.aruco.DetectorParameters_create() # default params
		self.tag = np.zeros((300, 300, 1), dtype="uint8")
		cv2.aruco.drawMarker(self.DICTIONARY, 10, 300, self.tag, 1)
		cv2.imwrite("images/test_tag.png", self.tag)
		
		# picamera params
		self.RESOLUTION = (1008,1008)
		self.FRAMERATE = 30

		# create VideoWriter object
		fourcc = cv2.VideoWriter_fourcc(*'XVID')
		self.vid = cv2.VideoWriter('images/output2.avi',fourcc, 20.0, self.RESOLUTION)


	def find_markers(self, frame):
		gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		corners, ids, _ = cv2.aruco.detectMarkers(gray_frame, self.DICTIONARY, parameters=self.PARAMETERS)

		result = [[], [], []]
		if ids is None:
			self.vid.write(frame)
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
			result[0].append(int(markerID))
			result[1].append(x_cent)
			result[2].append(width)
		# write frame to vid
		self.vid.write(frame)
		return result


	def execute(self):
		# create the camera
		camera = picamera.PiCamera()
		camera.resolution = self.RESOLUTION # (1008,1008)
		camera.framerate = self.FRAMERATE # 30

		# create the Robot
		car = Robot()

		rawCapture = picamera.array.PiRGBArray(camera, size=self.RESOLUTION)
		try:
			for capture in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
				frame = capture.array
				markers = self.find_markers(frame)
				
				print(markers)
				car.change_state(markers)
				car.act(markers)
				print(car.state)
				
				rawCapture.truncate(0)

		except KeyboardInterrupt:
			logging.exception("Keyboard interruption: exiting.")
		finally:
			camera.close()
			self.vid.release()
			io.cleanup()


if __name__ == "__main__":
	script = RunCar()
	script.execute()
