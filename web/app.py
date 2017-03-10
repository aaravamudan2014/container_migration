#!/usr/bin/env python
from flask import Flask, render_template, Response
import skvideo.io
#import skimage.io
import threading
import argparse
import cv2
import numpy as np
import datetime
import imutils
import time
import urllib, cStringIO
from flask import Flask
from time import sleep

app = Flask(__name__)
began = False
switch = False
frame = None
condition=threading.Event()
condition_shakehand = threading.Event()
def processor():
        # construct the argument parser and parse the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--video",help="path to the video file")
        ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
        args = vars(ap.parse_args())

        # otherwise, we are reading from a video file
        camera = skvideo.io.VideoCapture('mov.webm')
	global frame
        # initialize the first frame in the video stream
        firstFrame = None
        # loop over the frames of the video
        if not camera.isOpened(): 
		print "cannot open file"
	
	while not began:
		pass
	while (camera.isOpened()):
        #a grab the current frame and initialize the occupied/unoccupied
        # text

		global condition
#		global condition_shakehand
#		if condition_shakehand.wait():
		condition.clear()
	        ret, frame = camera.read()
                text = "Unoccupied"
        	
	        if not ret:
        	        print "video file reading complete or corrupted"
			camera.release()
			camera = skvideo.io.VideoCapture('mov.webm')
			ret, frame = camera.read()
        # resize the frame, convert it to grayscale, and blur it
                frame = imutils.resize(frame, width=500)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (21, 21), 0)
	
        # if the first frame is None, initialize it
                if firstFrame is None:
                        firstFrame = gray
                        continue
        # compute the absolute difference between the current frame and
        # first frame
                frameDelta = cv2.absdiff(firstFrame, gray)
                thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
	
                # dilate the thresholded image to fill in holes, then find contours
                # on thresholded image
                thresh = cv2.dilate(thresh, None, iterations=2)
                _,cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        # loop over the contours
                for c in cnts:
                # if the contour is too small, ignore it
                        if cv2.contourArea(c) < args["min_area"]:
                                continue

                # compute the bounding box for the contour, draw it on the frame,
                # and update the text
                        (x, y, w, h) = cv2.boundingRect(c)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        text = "Occupied"
        # draw the text and timestamp on the frame
                cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

		condition.set()
		sleep(0.02)
#		print "processed"
	#cleanup the camera and close any open windows
		
        camera.release()
        
def image_snatcher():
	global began
	began = True
	global frame
	global condition
	global condition_shakehand
	while True:
		if condition.wait():	
			condition.clear()
			yield (b'--frame\r\n'b'Content-Type: image/jpeg \r\n\r\n'+cv2.imencode('.jpg', frame)[1].tostring()+ b'\r\n')
#			condition_shakehand.set()
#			print "done with yielding"
			
	
#	condition.release()
@app.route("/")
def index():
	return render_template('index.html')


@app.route('/video_feed')
def video_feed():
	return Response(image_snatcher(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    


if __name__ == '__main__':
	t=threading.Thread(target=processor)
	t.daemon = True
	t.start()
	app.run(host='0.0.0.0',port=8000, use_reloader=True)


