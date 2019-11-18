# USAGE
# python motion_detector.py
# python motion_detector.py --video videos/example_01.mp4

# import the necessary packages
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2

import functions

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=700, help="minimum area size")
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
    vs = VideoStream(src=0).start()
    vs2 = VideoStream(src=1).start()
    time.sleep(2.0)
# otherwise, we are reading from a video file
else:
    vs = cv2.VideoCapture(args["video"])

# initialize the csv file
# headRow = ["object-number", "recorded-time", "run-time", "frame-number", "x-position", "y-position", "z-position"]
# functions.writeToCSV(headRow)

# frame counter (recorded in the CSV)
frameCount = 0

# initialize timer
# timer is set to 10 FPS
nextFrameTime = time.time() + 0.1
totalRunTime = time.time()

# initialize the first frame in the video stream
firstFrame = None
firstFrame2 = None

# loop over the frames of the video
while True:
    # grab the current frame and initialize the occupied/unoccupied
    # text
    frame = vs.read()
    frame = frame if args.get("video", None) is None else frame[1]
    text = "No movement"

    # if the frame could not be grabbed, then we have reached the end
    # of the video
    if frame is None:
        break

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
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # loop over the contours
    largestObjCount = 0
    largestObjSize = 0

    count = 1
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        if w*h > largestObjSize:
            largestObjSize = w*h
            largestObjCount = count
        count = count + 1

    objectCount = 0
    for c in cnts:
        objectCount = objectCount + 1;
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < args["min_area"]:
            continue

        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)

        #print("object count is: ", objectCount, "largest obj count is: ", largestObjCount)

        if objectCount == largestObjCount:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # # record the data in accordance to the timer
            # if nextFrameTime <= time.time():
            #     nextFrameTime = nextFrameTime + 0.1
            #     print("adding record to CSV")
            #     xPos = x + (w / 2)
            #     yPos = y + (h / 2)
            #     dataToRecord = [1, datetime.datetime.now(), time.time() - totalRunTime, frameCount, xPos,
            #                     yPos, 0]
            #     functions.appendToCSV(dataToRecord)
            #     frameCount = frameCount + 1
        else:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        text = "The fish is moving"

        # print out the x and y for each tracked object
        # print("Xpos :", x, "Ypos :", y)

    # draw the text and timestamp on the frame
    cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    ############ camera 2 #################

    # grab the current frame and initialize the occupied/unoccupied
    # text
    frame2 = vs2.read()
    text2 = "No movement"

    # if the frame could not be grabbed, then we have reached the end
    # of the video
    if frame2 is None:
        break

    # resize the frame, convert it to grayscale, and blur it
    frame2 = imutils.resize(frame2, width=500)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)

    # if the first frame is None, initialize it
    if firstFrame2 is None:
        firstFrame2 = gray2
        continue

    # compute the absolute difference between the current frame and
    # first frame
    frameDelta2 = cv2.absdiff(firstFrame2, gray2)
    thresh2 = cv2.threshold(frameDelta2, 25, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh2 = cv2.dilate(thresh2, None, iterations=2)
    cnts2 = cv2.findContours(thresh2.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts2 = imutils.grab_contours(cnts2)

    # loop over the contours
    largestObjCount2 = 0
    largestObjSize2 = 0

    count2 = 1
    for c2 in cnts2:
        (x2, y2, w2, h2) = cv2.boundingRect(c2)
        if w2 * h2 > largestObjSize2:
            largestObjSize2 = w2 * h2
            largestObjCount2 = count2
        count2 = count2 + 1

    objectCount2 = 0
    for c2 in cnts2:
        objectCount2 = objectCount2 + 1;
        # if the contour is too small, ignore it
        if cv2.contourArea(c2) < args["min_area"]:
            continue

        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x2, y2, w2, h2) = cv2.boundingRect(c2)

        # print("object count is: ", objectCount, "largest obj count is: ", largestObjCount)

        if objectCount2 == largestObjCount2:
            cv2.rectangle(frame2, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 0), 2)
            # record the data in accordance to the timer
            # if nextFrameTime <= time.time():
            #     nextFrameTime = nextFrameTime + 0.1
            #     print("adding record to CSV")
            #     xPos = x + (w / 2)
            #     yPos = y + (h / 2)
            #     dataToRecord = [1, datetime.datetime.now(), time.time() - totalRunTime, frameCount, xPos,
            #                     yPos, 0]
            #     functions.appendToCSV(dataToRecord)
            #     frameCount = frameCount + 1
        else:
            cv2.rectangle(frame2, (x2, y2), (x2 + w2, y2 + h2), (0, 0, 255), 2)

        text2 = "The fish is moving"

        # print out the x and y for each tracked object
        # print("Xpos :", x, "Ypos :", y)

    # draw the text and timestamp on the frame
    cv2.putText(frame2, "Room Status: {}".format(text2), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame2, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    ##### DISPLAY #####

    # show the frame and record if the user presses a key
    cv2.imshow("Camera 1", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    cv2.imshow("Camera 2", frame2)
    cv2.imshow("Thresh 2", thresh2)
    cv2.imshow("Frame Delta 2", frameDelta2)

    key = cv2.waitKey(1) & 0xFF

    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
        functions.averageCSV()
        exit()

# cleanup the camera and close any open windows
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()