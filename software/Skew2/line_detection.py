import numpy as np
import cv2

def prep_image(image):
    HSV_min = np.array([10, 0, 0], np.uint8)
    HSV_max = np.array([50, 255, 255], np.uint8)

    hsv = extract_colour(image, HSV_min, HSV_max, 1)
    median = cv2.medianBlur(hsv, 9)  # 3 is kernel size

    #bitwise_and(pic1, pic2, mask)
    anded = cv2.bitwise_and(image, image, mask = median)
    cv2.imshow("asd", anded)
    cv2.imshow("hsv", median)
    cv2.waitKey(0)
    return median

def extract_colour(image, low, high, binary):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    threshold = cv2.inRange(hsv, low, high)
    if binary:
        return threshold
    else:
        #temporarily putting return full image here
        return cv2.bitwise_and(image, image, mask = threshold)

def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged

def a():
    img = cv2.imread("zipcar.jpg")
    img2 = img

    img = prep_image(img)

    laplacian = cv2.Laplacian(img,cv2.CV_64F)

    sobel = cv2.Sobel(laplacian, cv2.CV_64F, 1, 1, ksize=5)
    abs_sobel64f = np.absolute(sobel)
    sobel_8u = np.uint8(abs_sobel64f)

    canny = cv2.Canny(img, 150, 200, 3)
    canny_auto = auto_canny(img)

    cv2.imshow("sobel", canny)
    cv2.imshow("sobel2", canny_auto)

    lines = cv2.HoughLinesP(canny_auto, 1, np.pi/180, 30, 300, 50)
    print(len(lines))
    print(lines)

    #draw lines on the best hough lines
    for i in range(len(lines)):
        for x1,y1,x2,y2 in lines[i]:
            cv2.line(img2, (x1, y1), (x2, y2), (0, 0, 255), 5)

    cv2.imshow('houghlines',img2)


    cv2.waitKey(0)
