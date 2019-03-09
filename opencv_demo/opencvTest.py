import cv2 as cv
import numpy as np
import time

cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_EXPOSURE, -9)
cap.set(cv.CAP_PROP_BRIGHTNESS, 127)
print(cap.get(cv.CAP_PROP_BRIGHTNESS))
while True:
    img = cap.read()[1]
    cv.imshow('', img)
    cv.waitKey(10)
    time.sleep(1)

# cap = cv.VideoCapture(0)
# while True:
#     _, img = cap.read()
#     gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
#     edges = cv.Canny(gray,50,150,apertureSize = 3)
#     lines = cv.HoughLinesP(edges,1,np.pi/180,100,minLineLength=100,maxLineGap=10)
#
#     slope = []
#     for line in lines:
#         x1,y1,x2,y2 = line[0]
#         if x1 != x2:
#             slope.append((y2 - y1) / (x2 - x1))
#     slope = np.array(slope, dtype=np.float32)
#
#     # Define criteria = ( type, max_iter = 10 , epsilon = 1.0 )
#     criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.1)
#     # Set flags (Just to avoid line break in the code)
#     flags = cv.KMEANS_RANDOM_CENTERS
#     # Apply KMeans
#     compactness,labels,centers = cv.kmeans(slope,2,None,criteria,20,flags)
#
#     x0 = img.shape[1] // 2
#     y0 = img.shape[0] // 2
#     for center in centers:
#         cos = 1 / ((1 + center ** 2) ** 0.5)
#         if center > 0 :
#             sin = (1 - cos ** 2) ** 0.5
#         else:
#             sin = - (1 - cos ** 2) ** 0.5
#         cv.line(img, (x0 - 100 * cos, y0 - 100 * sin), (x0 + 100 * cos, y0 + 100 * sin), (0, 255, 0), 2)
#     for line in lines:
#         x1,y1,x2,y2 = line[0]
#         cv.line(img,(x1,y1),(x2,y2),(255,0,0),2)
#     cv.imshow('', img)
#     k = cv.waitKey(60)

#cap = cv.VideoCapture(0)
## take first frame of the video
#ret,frame = cap.read()
## setup initial location of window
#r,h,c,w = 250,90,400,125  # simply hardcoded the values
#track_window = (c,r,w,h)
## set up the ROI for tracking
#roi = frame[r:r+h, c:c+w]
#hsv_roi =  cv.cvtColor(roi, cv.COLOR_BGR2HSV)
#mask = cv.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
#roi_hist = cv.calcHist([hsv_roi],[0],mask,[180],[0,180])
#cv.normalize(roi_hist,roi_hist,0,255,cv.NORM_MINMAX)
## Setup the termination criteria, either 10 iteration or move by atleast 1 pt
#term_crit = ( cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1 )
#while(1):
#    ret ,frame = cap.read()
#    if ret == True:
#        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
#        dst = cv.calcBackProject([hsv],[0],roi_hist,[0,180],1)
#        # apply meanshift to get the new location
#        ret, track_window = cv.meanShift(dst, track_window, term_crit)
#        # Draw it on image
#        x,y,w,h = track_window
#        img2 = cv.rectangle(frame, (x,y), (x+w,y+h), 255,2)
#        cv.imshow('img2',img2)
#        k = cv.waitKey(60) & 0xff
#        if k == 27:
#            break
#        else:
#            cv.imwrite(chr(k)+".jpg",img2)
#    else:
#        break
#cv.destroyAllWindows()
#cap.release()

#import time
#import cv2 as cv

#cap = cv.VideoCapture(0)
#while True:
#        time1 = time.perf_counter()
#        _, frame = cap.read()
#        time2 = time.perf_counter()
#        print(str((time2 - time1) * 1000) + 'ms ' + str(1 / (time2 - time1)) + 'Hz')
