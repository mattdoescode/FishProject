# USAGE
# python multi_object_tracking.py --video videos/soccer_01.mp4 --tracker csrt

# import the necessary packages
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import threading

import functions

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
                help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="kcf",
                help="OpenCV object tracker type")
args = vars(ap.parse_args())

# initialize a dictionary that maps strings to their corresponding
# OpenCV object tracker implementations
OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    "boosting": cv2.TrackerBoosting_create,
    "mil": cv2.TrackerMIL_create,
    "tld": cv2.TrackerTLD_create,
    "medianflow": cv2.TrackerMedianFlow_create,
    "mosse": cv2.TrackerMOSSE_create
}

# initialize OpenCV's special multi-object tracker
trackers = cv2.MultiTracker_create()

# initialize the csv file
headRow = ["time", "frame number", "cam number", "x position", "y position", "z position"]
functions.writeToCSV(headRow)

# we don't need any of this right now
# if a video path was not supplied, grab the reference to the web cam
# if not args.get("video", False):
#    print("[INFO] starting video stream...")
#    vs = VideoStream(src=0).start()
#    time.sleep(1.0)

# otherwise, grab a reference to the video file
#else:
#   vs = cv2.VideoCapture(args["video"])

class camThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
    def run(self):
        print("Starting " + self.previewName)
        camPreview(self.previewName, self.camID)

# we need vs -> videostream

def camPreview(previewName, camID):
    # cv2.namedWindow(previewName)
    vs = VideoStream(camID).start()
    time.sleep(1.0)

    # frame counter (recorded in the CSV)
    frameCount = 0

    # loop over frames from the video stream
    while True:
        # grab the current frame, then handle if we are using a
        # VideoStream or VideoCapture object
        frame = vs.read()
        frame = frame[1] if args.get("video", False) else frame

        # check to see if we have reached the end of the stream
        if frame is None:
            print("frame is done")
            break

        # resize the frame (so we can process it faster)
        frame = imutils.resize(frame, width=700)

        # grab the updated bounding box coordinates (if any) for each
        # object that is being tracked
        (success, boxes) = trackers.update(frame)

        # loop over the bounding boxes and draw then on the frame
        for box in boxes:
            (x, y, w, h) = [int(v) for v in box]
            # image = cv2.rectangle(image, start_point, end_point, color, thickness)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # our center point is
            xPos = x + (w / 2)
            yPos = y + (h / 2)

            #print out the x and y for each tracked object
            # print("Xpos :", x, "Ypos :", y)

            # record the data and
            dataToRecord = [0, frameCount, xPos, yPos, 0]
            functions.appendToCSV(dataToRecord)

            frameCount = frameCount + 1


        # print("Frame count: ", frameCount)
        cv2.imshow(previewName, frame)

        key = cv2.waitKey(1) & 0xFF

        # if the 's' key is selected, we are going to "select" a bounding
        # box to track
        if key == ord("s"):
            # select the bounding box of the object we want to track (make
            # sure you press ENTER or SPACE after selecting the ROI)
            box = cv2.selectROI("Frame", frame, fromCenter=False,
                                showCrosshair=True)

            # create a new object tracker for the bounding box and add it
            # to our multi-object tracker
            tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
            trackers.add(tracker, frame, box)

        # if the `q` key was pressed, break from the loop
        elif key == ord("q"):
            break
    cv2.destroyWindow(previewName)
    # end of true loop
    # if we are using a webcam, release the pointer
    #if not args.get("video", False):
    #   vs.stop()

    # otherwise, release the file pointer
    #else:
    #   vs.release()

    # close all windows



# Create two threads as follows
thread1 = camThread("Camera 1", 0)
thread2 = camThread("Camera 2", 1)
thread1.start()
thread2.start()
