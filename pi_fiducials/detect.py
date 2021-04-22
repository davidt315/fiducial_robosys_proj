import numpy as np
import cv2

import picamera
import picamera.array

DICTIONARY = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250) # our marker dictionary
tag = np.zeros((300, 300, 1), dtype="uint8")
cv2.aruco.drawMarker(DICTIONARY, 10, 300, tag, 1)
cv2.imwrite("test_tag.png", tag)

PARAMETERS = cv2.aruco.DetectorParameters_create() # default params
MARKER_EDGE = 0.05 # not really relevant for our use case; our marker size is 5cm x 5cm

RESOLUTION = (1008,1008)
FRAMERATE = 30


def find_markers(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, DICTIONARY, parameters=PARAMETERS)
    # rvecs, tvecs, _objPoints = cv2.aruco.estimatePoseSingleMarkers(corners, MARKER_EDGE, CAMERA_MATRIX, DIST_COEFFS)

    result = set()
    if ids is None:
        return result

    for i in range(0, len(ids)):
        try:
            id = str(ids[i][0])

            marker = np.squeeze(corners[i])

            x1,y1 = marker[0]
            x2,y2 = marker[2]
            x = int((x1 + x2)/2)
            y = int((y1 + y2)/2)

            # bearing = calc_heading(rvecs[i][0])
            result.add((id, x, y))  #, bearing))
        except Exception:
            print("error on marker")

    return result



camera = picamera.PiCamera()
camera.resolution = RESOLUTION # (1008,1008)
camera.framerate = FRAMERATE # 30

rawCapture = picamera.array.PiRGBArray(camera, size=RESOLUTION)

camera.start_recording('testing.h264')
try:
    for capture in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        frame = capture.array
        markers = find_markers(frame)

        print(markers)

        rawCapture.truncate(0) 
except:
    print("error on capture")
finally:
    camera.stop_recording()
    camera.close()