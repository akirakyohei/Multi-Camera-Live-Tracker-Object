from __future__ import division, print_function, absolute_import

import cv2
from base_camera import BaseCamera

import warnings
import numpy as np
from PIL import Image
from single_motion_detector import SingleMotionDetector
from importlib import import_module
from collections import Counter
import datetime
import imutils

warnings.filterwarnings('ignore')


class Camera(BaseCamera):
    def __init__(self, feed_type, device, port_list):
        super(Camera, self).__init__(feed_type, device, port_list)
        

    @staticmethod
    def yolo_frames(unique_name):
        device = unique_name[1]

        tracking = True

        if tracking:
	        # initialize the motion detector and the total number of frames
	        # read thus far
            md = SingleMotionDetector(accumWeight=0.1)
            total = 0
	        # loop over frames from the video stream
            get_feed_from = ('camera', device)
            while True:
	        	# read the next frame from the video stream, resize it,
	        	# convert the frame to grayscale, and blur it
                cam_id, frame = BaseCamera.get_frame(get_feed_from)
                frame = imutils.resize(frame, width=400)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (7, 7), 0)
	        	# grab the current timestamp and draw it on the frame
                timestamp = datetime.datetime.now()
                # cv2.putText(frame, timestamp.strftime(
	        	# 	"%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
		    	# cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    
		    # if the total number of frames has reached a sufficient
		    # number to construct a reasonable background model, then
		    # continue to process the frame
            #if total > frameCount:
                if total > 0:
		    	    # detect motion in the image
                    motion = md.detect(gray)
		    	# check to see if motion was found in the frame
                    if motion is not None:
		    		# unpack the tuple and draw the box surrounding the
		    		# "motion area" on the output frame
                        (thresh, (minX, minY, maxX, maxY)) = motion
                        cv2.rectangle(frame, (minX, minY), (maxX, maxY),
		    			(0, 0, 255), 2)
                        
    
		    # update the background model and increment the total number
		    # of frames read thus far
                md.update(gray)
                total += 1   
                yield cam_id, frame