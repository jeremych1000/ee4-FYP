import cv2
import datetime
import time
import imutils

camera = cv2.VideoCapture(0)
#camera = cv2.VideoCapture("test_files/parking_lot_1.mp4")
time.sleep(0.25)

#min area for considering motion in pixels
minArea = 10000


#assume first frame is just background
firstFrame = None

while True:
    (gradFrame_success, frame) = camera.read()
    if not gradFrame_success:
        break #fail to get frame

    displayText = "No motion"

    frame = imutils.resize(frame, width=1500)
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grey = cv2.GaussianBlur(grey, (21, 21), 0)

    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = grey
        continue

    frameDiff = cv2.absdiff(firstFrame, grey)
    threshold = cv2.threshold(frameDiff, 25, 255, cv2.THRESH_BINARY)[1]

    #dilate to fill in holes
    dilated = cv2.dilate(threshold, None, iterations = 2)
    dilated_copy = dilated
    (im2, cnts, hier) = cv2.findContours(dilated_copy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #CHAIN APPROX SIMPLE only gives corner coodinates, and not the whole line

    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < minArea:
            continue

        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        displayText = "MOTION!!!!!!!!!!!!!!"

    # draw the text and timestamp on the frame
    # image, position x y, font, size, colour, thickness
    cv2.putText(frame, displayText, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    # show the frame and record if the user presses a key
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Thresh", threshold)
    cv2.imshow("Frame Delta", frameDiff)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()