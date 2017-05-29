import tkinter as tk
import numpy as np
import cv2
import imutils
import time

from warp_image import warp
from alpr import get_plates
from line_detection import extract_colour
from motion import detect_motion

type = "video" #or video

print("top")
if type is "image":
    ret, input_file = cv2.imread("test_files/g1w.png")
    if not ret:
        print("Failed to read image")
    frame = input_file #needed as img is either image or video
    #need to add check for image successful read or not
    rows,cols,ch = input_file.shape
else:
    #need to add check for image successful read or not
    input_file = cv2.VideoCapture("F:/test_videos/walking/VID_20170529_003059.mp4")
    cols = input_file.get(3)
    rows = input_file.get(4)

    ret, first_frame = input_file.read()
    if not ret:
        print("Failed to read video")
    cv2.imshow("first frame", first_frame)
    #frame = first_frame #needed as img is either image or video

def task():
    print("Doing task")
    #get tkintvar values
    tl = (warp1.get(), warp2.get())
    tr = (warp3.get(), warp4.get())
    bl = (warp5.get(), warp6.get())
    br = (warp7.get(), warp8.get())
    pts = [ (tl[0], tl[1]), (tr[0], tr[1]), (bl[0], bl[1]), (br[0], br[1]) ]
    HSV_min = np.array([h1.get(), s1.get(), v1.get()], np.uint8)
    HSV_max = np.array([h2.get(), s2.get(), v2.get()], np.uint8)
    r_angle = rotate_angle.get()
    curr_frame.set(curr_frame.get() + 1)
    print("Current frame is %u" % curr_frame.get())

    if type is "video":
        ret, frame = input_file.read()
        cv2.imshow("current frame", frame)

    is_motion, motion_frame = detect_motion(first_frame, frame, 10000, int(cols))

    #need to add histogram equalization too

    rotated = imutils.rotate(motion_frame, r_angle)
    warped = warp(rotated, pts)
    hsv = extract_colour(warped, HSV_min, HSV_max, 0)
    cv2.imwrite("tmp_output.jpg", hsv)

    cv2.imshow("output", hsv)

    if is_motion:
        get_plates("tmp_output.jpg", "eu", 3)

    print("---")

    #schedule tasks to run instead of using time.sleep
    root.after(update_interval.get(), task)

root = tk.Tk()
root.title("Prewarp image")

tk.Label(root, text="Top Left").grid(row=0, column=0)
tk.Label(root, text="Top Right").grid(row=1, column=0)
tk.Label(root, text="Bottom Left").grid(row=2, column=0)
tk.Label(root, text="Bottom Right").grid(row=3, column=0)
tk.Label(root, text="HSV Low").grid(row=4, column=0)
tk.Label(root, text="HSV High").grid(row=5, column=0)
tk.Label(root, text="Rotation Angle").grid(row=6, column=0)
tk.Label(root, text="Update Interval").grid(row=7, column=0)

tl = (tk.IntVar(), tk.IntVar())
tr = (tk.IntVar(), tk.IntVar())
bl = (tk.IntVar(), tk.IntVar())
br = (tk.IntVar(), tk.IntVar())
h = (tk.IntVar(), tk.IntVar())
s = (tk.IntVar(), tk.IntVar())
v = (tk.IntVar(), tk.IntVar())
rotate_angle = tk.IntVar()
update_interval = tk.IntVar()
curr_frame = tk.IntVar()
curr_frame.set(0)

#http://effbot.org/tkinterbook/grid.htm
warp1 = tk.Scale(root, orient='horizontal', from_=0, to=cols)
warp1.set(0)
warp1.grid(row=0, column=1)
warp2 = tk.Scale(root, orient='horizontal', from_=0, to=rows)
warp2.set(0)
warp2.grid(row=0, column=2)

warp3 = tk.Scale(root, orient='horizontal', from_=0, to=cols)
warp3.set(0)
warp3.grid(row=1, column=1)
warp4 = tk.Scale(root, orient='horizontal', from_=0, to=rows)
warp4.set(rows)
warp4.grid(row=1, column=2)

warp5 = tk.Scale(root, orient='horizontal', from_=0, to=cols)
warp5.set(cols)
warp5.grid(row=2, column=1)
warp6 = tk.Scale(root, orient='horizontal', from_=0, to=rows)
warp6.set(0)
warp6.grid(row=2, column=2)

warp7 = tk.Scale(root, orient='horizontal', from_=0, to=cols)
warp7.set(cols)
warp7.grid(row=3, column=1)
warp8 = tk.Scale(root, orient='horizontal', from_=0, to=rows)
warp8.set(cols)
warp8.grid(row=3, column=2)

h1 = tk.Scale(root, orient='horizontal', from_=0, to=179)
h1.set(0)
h1.grid(row=4, column=1)
s1 = tk.Scale(root, orient='horizontal', from_=0, to=255)
s1.set(0)
s1.grid(row=4, column=2)
v1 = tk.Scale(root, orient='horizontal', from_=0, to=255)
v1.set(0)
v1.grid(row=4, column=3)

h2 = tk.Scale(root, orient='horizontal', from_=0, to=179)
h2.set(179)
h2.grid(row=5, column=1)
s2 = tk.Scale(root, orient='horizontal', from_=0, to=255)
s2.set(255)
s2.grid(row=5, column=2)
v2 = tk.Scale(root, orient='horizontal', from_=0, to=255)
v2.set(255)
v2.grid(row=5, column=3)

rot_angle = tk.Scale(root, orient='horizontal', from_=0, to=360, var=rotate_angle)
rot_angle.set(0)
rot_angle.grid(row=6, column=1)

update_scale = tk.Scale(root, orient='horizontal', from_=1, to=1000, var=update_interval)
update_scale.set(1000)
update_scale.grid(row=7, column=1)

root.after(update_interval.get(), task)
root.mainloop()