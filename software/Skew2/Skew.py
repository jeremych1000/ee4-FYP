import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from warp_image import four_point_transform

#try and mimic http://doc.openalpr.com/accuracy_improvements.html prewarping
def warp(img, pts):

    print("Entering warp function with parameters %d %d %d %d" % (pts[0][0], pts[0][1], pts[1][0], pts[1][1]))
    #img = cv2.imread("zipcar.jpg")
    rows,cols,ch = img.shape

    #cv2.imshow("Original", img)

    #points = "[(892, 395), (1085, 331), (910, 485), (1114, 555)]"
    #points = "[(96,15), (588, 132), (113, 504), (633, 452)]"
    pts = np.array(pts, dtype = "float32")

    warped = four_point_transform(img, pts, rows, cols, True)

    #cv2.imshow("warped", warped)

    #pts1 = np.float32([[50,50],[200,50],[50,200]])
    #pts2 = np.float32([[10,100],[200,50],[100,250]])
    #
    #M = cv2.getAffineTransform(pts1,pts2)
    #
    #dst = cv2.warpAffine(img,M,(cols,rows))
    #
    #plt.subplot(121),plt.imshow(img),plt.title('Input')
    #plt.subplot(122),plt.imshow(dst),plt.title('Output')
    #plt.show()

    #cv2.waitKey(0)
    return warped