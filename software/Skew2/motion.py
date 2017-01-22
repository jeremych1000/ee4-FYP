import cv2
import datetime
import imutils

def detect_motion(first, current, min_area = 10000, resize_width = 1000):
    displayText = "---------"
    motion_detected = False

    #first_frame = imutils.resize(first, width=resize_width)
    #current_frame = imutils.resize(current, width = resize_width)

    #preprocess image for absdiff
    first_grey = cv2.cvtColor(first, cv2.COLOR_BGR2GRAY)
    first_grey = cv2.GaussianBlur(first_grey, (21, 21), 0)
    grey = cv2.cvtColor(current, cv2.COLOR_BGR2GRAY)
    grey = cv2.GaussianBlur(grey, (21, 21), 0)

    frameDiff = cv2.absdiff(first_grey, grey)
    threshold = cv2.threshold(frameDiff, 25, 255, cv2.THRESH_BINARY)[1]

    #dilate to fill in holes
    dilated = cv2.dilate(threshold, None, iterations = 2)
    dilated_copy = dilated
    (im2, cnts, hier) = cv2.findContours(dilated_copy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #CHAIN APPROX SIMPLE only gives corner coodinates, and not the whole line

    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < min_area:
            continue

        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(current, (x, y), (x + w, y + h), (0, 255, 0), 2)
        displayText = "!!!!!!!!!!!"
        motion_detected =  True

    # draw the text and timestamp on the frame
    # image, position x y, font, size, colour, thickness
    cv2.putText(current, displayText, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(current, datetime.datetime.now().strftime("%d %B %Y %I:%M:%S%p"), (10, current.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    # show the frame and record if the user presses a key
    #cv2.imshow("Security Feed", frame)
    #cv2.imshow("Thresh", threshold)
    #cv2.imshow("Frame Delta", frameDiff)

    return motion_detected, current