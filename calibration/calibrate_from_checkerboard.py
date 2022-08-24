# print checkerboard
# easy generation of checkerboard http://kr.mathworks.com/help/images/ref/checkerboard.html

import cv2
import numpy as np
import os
# import glob
import imageio 
 
VIDEO_DIRECTORY = 'iphoneXR.mov'
OUTPUT_CONFIG = 'iphoneXR.yaml'
# Define the dimensions of 'corners' in checkerboard, checkerboard.png in this directory is 9, 9
CHECKERBOARD = (9, 9)
 
# stop the iteration when specified
# accuracy, epsilon, is reached or
# specified number of iterations are completed.
criteria = (cv2.TERM_CRITERIA_EPS +
            cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
 
 
# Vector for 3D points
threedpoints = []
 
# Vector for 2D points
twodpoints = []
 
 
#  3D points real world coordinates
objectp3d = np.zeros((1, CHECKERBOARD[0]
                      * CHECKERBOARD[1],
                      3), np.float32)
objectp3d[0, :, :2] = np.mgrid[0:CHECKERBOARD[0],
                               0:CHECKERBOARD[1]].T.reshape(-1, 2)
prev_img_shape = None
 
 
# Extracting path of individual image stored
# in a given directory. Since no path is
# specified, it will take current directory
# jpg files alone

imgs = []
reader = imageio.get_reader(VIDEO_DIRECTORY)
print(reader.get_meta_data())
print(reader.get_meta_data()['fps'])
for i, im in enumerate(reader):
    # imgs.append(im)
    imgs.append(im)

imgs = np.array(imgs)
num_frames, H, W, C = imgs.shape
print(num_frames, H, W, C)
images = imgs[::int(np.ceil(num_frames / 50))]
num_frames, H, W, C = images.shape
print(num_frames, H, W, C)

 
# for filename in images:
for i, image in enumerate(images):
    print(f'processing frame {i} out of {images.shape[0]}')
    # image = cv2.imread(filename)
    grayColor = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
    # Find the chess board corners
    # If desired number of corners are
    # found in the image then ret = true
    ret, corners = cv2.findChessboardCorners(
                    grayColor, CHECKERBOARD,
                    cv2.CALIB_CB_ADAPTIVE_THRESH
                    + cv2.CALIB_CB_FAST_CHECK +
                    cv2.CALIB_CB_NORMALIZE_IMAGE)
 
    # If desired number of corners can be detected then,
    # refine the pixel coordinates and display
    # them on the images of checker board
    if ret == True:
        threedpoints.append(objectp3d)
 
        # Refining pixel coordinates
        # for given 2d points.
        corners2 = cv2.cornerSubPix(
            grayColor, corners, (11, 11), (-1, -1), criteria)
 
        twodpoints.append(corners2)
 
        # Draw and display the corners
        # image = cv2.drawChessboardCorners(image,
        #                                   CHECKERBOARD,
        #                                   corners2, ret)
 
    # cv2.imshow('img', image)
    # cv2.waitKey(0)
 
h, w = image.shape[:2]
 
 
# Perform camera calibration by
# passing the value of above found out 3D points (threedpoints)
# and its corresponding pixel coordinates of the
# detected corners (twodpoints)
ret, matrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera(
    threedpoints, twodpoints, grayColor.shape[::-1], None, None)
 
 
# Displaying required output
print(" Camera matrix:")
print(matrix, matrix.shape)
 
print("\n Distortion coefficient:")
print(distortion, distortion.shape)

# print("\n Rotation Vectors:")
# print(r_vecs)
 
# print("\n Translation Vectors:")
# print(t_vecs)

fx = matrix[0][0]
fy = matrix[1][1]
cx = matrix[0][2]
cy = matrix[1][2]
k1 = distortion[0][0]
k2 = distortion[0][1]
p1 = distortion[0][2]
p2 = distortion[0][3]
fps = reader.get_meta_data()['fps']

with open(OUTPUT_CONFIG, 'w') as f:
    f.write("%YAML:1.0\n")
    f.write(f"Camera.fx: {fx}\n")
    f.write(f"Camera.fy: {fy}\n")
    f.write(f"Camera.cx: {cx}\n")
    f.write(f"Camera.cy: {cy}\n")

    f.write(f"Camera.k1: {k1}\n")
    f.write(f"Camera.k2: {k2}\n")
    f.write(f"Camera.p1: {p1}\n")
    f.write(f"Camera.p2: {p2}\n")

    f.write(f"Camera.fps: {fps}\n")

    f.write("Camera.RGB: 1\n")

    f.write("#--------------------------------------------------------------------------------------------\n")
    f.write("# ORB Parameters\n")
    f.write("#--------------------------------------------------------------------------------------------\n")

    f.write("ORBextractor.nFeatures: 2000\n")

    f.write("ORBextractor.scaleFactor: 1.2\n")

    f.write("ORBextractor.nLevels: 8\n")

    f.write("ORBextractor.iniThFAST: 20\n")
    f.write("ORBextractor.minThFAST: 7\n")

    f.write("Viewer.KeyFrameSize: 0.1\n")
    f.write("Viewer.KeyFrameLineWidth: 1\n")
    f.write("Viewer.GraphLineWidth: 1\n")
    f.write("Viewer.PointSize: 2\n")
    f.write("Viewer.CameraSize: 0.15\n")
    f.write("Viewer.CameraLineWidth: 2\n")
    f.write("Viewer.ViewpointX: 0\n")
    f.write("Viewer.ViewpointY: -10\n")
    f.write("Viewer.ViewpointZ: -0.1\n")
    f.write("Viewer.ViewpointF: 2000\n")

