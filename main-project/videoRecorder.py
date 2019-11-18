import cv2
import numpy as np

# Create a VideoCapture object
cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Unable to read camera feed")

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
frame_width2 = int(cap2.get(3))
frame_height2 = int(cap2.get(4))

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
out = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 20, (frame_width, frame_height))
out2 = cv2.VideoWriter('outpy2.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 20, (frame_width2, frame_height2))

while True:
    ret, frame = cap.read()
    if ret:
        # Write the frame into the file 'output.avi'
        out.write(frame)

        # Display the resulting frame
        cv2.imshow('frame', frame)

        # Press Q on keyboard to stop recording
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    ret2, frame2 = cap2.read()
    if ret2:
        # Write the frame into the file 'output.avi'
        out2.write(frame2)

        # Display the resulting frame
        cv2.imshow('frame2', frame2)

        # Press Q on keyboard to stop recording
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Break the loop
    else:
        break

    # When everything done, release the video capture and video write objects
cap.release()
out.release()
cap2.release()
out2.release()

# Closes all the frames
cv2.destroyAllWindows()
