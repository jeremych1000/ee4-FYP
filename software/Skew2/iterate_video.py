import cv2, sys
from openalpr import Alpr
from alpr import get_plates

vidcap = cv2.VideoCapture("F:/test_videos/walking/VID_20170528_200924.mp4")

count = 0
success = True
while success:
    success, image = vidcap.read()
    print("Reading ", count, "th frame: ", success)
    name = "frame" + str(count) + ".jpg"

    cv2.imwrite("t.jpg", image)  # save frame as JPEG file
    get_plates(input="t.jpg")

    count += 1
