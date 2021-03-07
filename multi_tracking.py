# import the necessary packages
from imutils.video import VideoStream ,FileVideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2
import numpy as np

optical_flow_sw = False

def draw_flow(im, flow, step=128):
    h, w = im.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1).astype(int)
    fx, fy = flow[y,x].T

    lines = np.vstack([x,y,x+fx, y+fy]).T.reshape(-1,2,2)
    lines = np.int32(lines)

    vis = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
    for (x1,y1) ,(x2,y2) in lines:
        cv2.line(vis, (x1,y1), (x2, y2), (0,255,0), 1)
        cv2.circle(vis, (x1,y1),1,(0,255,0),-1)
    return vis

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
                help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="csrt",
                help="OpenCV object tracker type")
args = vars(ap.parse_args())

# extract the OpenCV version info
(major, minor) = cv2.__version__.split(".")[:2]
# if we are using OpenCV 3.2 OR BEFORE, we can use a special factory
# function to create our object tracker
if int(major) == 3 and int(minor) < 3:
    tracker = cv2.Tracker_create(args["tracker"].upper())
# otherwise, for OpenCV 3.3 OR NEWER, we need to explicity call the
# approrpiate object tracker constructor:
else:
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
    # grab the appropriate object tracker using our dictionary of
    # OpenCV object tracker objects
    trackers = cv2.MultiTracker_create()
# tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
# initialize the bounding box coordinates of the object we are going
# to track
initBB = None
objectIDs=[1,2,3,4,5,6,7,8,9,10]
# if a video path was not supplied, grab the reference to the web cam
if not args.get("video", False):
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    time.sleep(1.0)
# otherwise, grab a reference to the video file
else:
    vs = cv2.VideoCapture(args["video"])
    #vs = FileVideoStream(args["video"]).start()
# initialize the FPS throughput estimator
fps = None
fps = FPS().start()
frames = []

if optical_flow_sw:
    frame = vs.read()
    frame = frame[1] if args.get("video", False) else frame
    frame = imutils.resize(frame, width=1600)
    prev_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# loop over frames from the video stream
while True:
    # grab the current frame, then handle if we are using a
    # VideoStream or VideoCapture object
    frame = vs.read()
    frame = frame[1] if args.get("video", False) else frame
    # check to see if we have reached the end of the stream
    if frame is None:
        break
    # resize the frame (so we can process it faster) and grab the
    # frame dimensions
    frame = imutils.resize(frame, width=1600)
    (H, W) = frame.shape[:2]
    frames.append(frame)
    fps.update()
    fps.stop()
    # initialize the set of information we'll be displaying on
    # the frame
    info = [
        ("Tracker", args["tracker"]),
        ("FPS", "{:.2f}".format(fps.fps())),
    ]
    # loop over the info tuples and draw them on our frame
    for (i, (k, v)) in enumerate(info):
        text = "{}: {}".format(k, v)
        cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    # check to see if we are currently tracking an object
    objectID=None
        # grab the new bounding box coordinates of the object
    (success, boxes) = trackers.update(frame)
        # check to see if the tracking was a success
        # if success:
    for box,objectID in zip(boxes,objectIDs):
        (x, y, w, h) = [int(v) for v in box]
        cv2.rectangle(frame, (x, y), (x + w, y + h),
                        (0, 255, 0), 2)
        text = "ID {}".format(objectIDs[objectID-1])
        cv2.putText(frame, text, (x,y),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
    

    if optical_flow_sw:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5,3,15,3,5,1.2,0)
        prev_gray = gray
        # show the output frame
        cv2.imshow("Frame", draw_flow(gray, flow))
    else:
        cv2.imshow("Frame", frame)

    key = cv2.waitKey(100) & 0xFF
    # if the 's' key is selected, we are going to "select" a bounding
    # box to track
    if key == ord("s"):
        # select the bounding box of the object we want to track (make
        # sure you press ENTER or SPACE after selecting the ROIs)
        box= cv2.selectROIs("Frame", frame, fromCenter=False,
                               showCrosshair=True)
        #change selectROIs type to selectROI
        box=tuple (map (tuple,box))
        #for loop tracks add each tracker box
        for bb in box:
            tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
            trackers.add(tracker, frame, bb)
    # if the `q` key was pressed, break from the loop
    elif key == ord("q"):
        break

    # key == ord("d"):
#if we are using a webcam, release the pointer
if not args.get("video", False):
    vs.stop()
# otherwise, release the file pointer
else:
    vs.release()
# close all windows
cv2.destroyAllWindows()

frames = np.array(frames)
print(frames.shape)

