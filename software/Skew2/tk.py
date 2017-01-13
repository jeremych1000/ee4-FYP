import tkinter as tk
import numpy as np
import cv2
from Skew import warp as www

img = cv2.imread("zipcar.jpg")
rows,cols,ch = img.shape


def task():
    tl = (s1.get(), s2.get())
    tr = (s3.get(), s4.get())
    bl = (s5.get(), s6.get())
    br = (s7.get(), s8.get())
    pts = [ (tl[0], tl[1]), (tr[0], tr[1]), (bl[0], bl[1]), (br[0], br[1]) ]
    output = www(img, pts)
    #print("slider numbners are %d %d %d %d" % (tl, tr, bl, br))
    cv2.imshow("output", output)
    root.after(update_interval.get(), task)

root = tk.Tk()
root.title("Prewarp image")

tk.Label(root, text="Top Left").grid(row=0, column=0)
tk.Label(root, text="Top Right").grid(row=1, column=0)
tk.Label(root, text="Bottom Left").grid(row=2, column=0)
tk.Label(root, text="Bottom Right").grid(row=3, column=0)
tk.Label(root, text="Update Interval").grid(row=4, column=0)

tl = (tk.IntVar(), tk.IntVar())
tr = (tk.IntVar(), tk.IntVar())
bl = (tk.IntVar(), tk.IntVar())
br = (tk.IntVar(), tk.IntVar())
update_interval = tk.IntVar()

s1 = tk.Scale(root, orient='horizontal', from_=0, to=cols)
s1.set(0)
s1.grid(row=0, column=1)
s2 = tk.Scale(root, orient='horizontal', from_=0, to=rows)
s2.set(0)
s2.grid(row=0, column=2)

s3 = tk.Scale(root, orient='horizontal', from_=0, to=cols)
s3.set(0)
s3.grid(row=1, column=1)
s4 = tk.Scale(root, orient='horizontal', from_=0, to=rows)
s4.set(rows)
s4.grid(row=1, column=2)

s5 = tk.Scale(root, orient='horizontal', from_=0, to=cols)
s5.set(cols)
s5.grid(row=2, column=1)
s6 = tk.Scale(root, orient='horizontal', from_=0, to=rows)
s6.set(0)
s6.grid(row=2, column=2)

s7 = tk.Scale(root, orient='horizontal', from_=0, to=cols)
s7.set(cols)
s7.grid(row=3, column=1)
s8 = tk.Scale(root, orient='horizontal', from_=0, to=rows)
s8.set(cols)
s8.grid(row=3, column=2)

update_scale = tk.Scale(root, orient='horizontal', from_=100, to=2000, var=update_interval)
update_scale.set(1000)
update_scale.grid(row=4, column=1)

root.after(update_interval.get(), task)
root.mainloop()