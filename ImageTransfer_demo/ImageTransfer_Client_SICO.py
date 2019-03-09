
import cv2 as cv
import socket
import numpy as np

cap = cv.VideoCapture(0)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#bsize = s.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
#print("Buffer size [After] : %d" % bsize)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 500000)
#bsize = s.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
#print("Buffer size [After] : %d" % bsize)

while True: 
    buf = cv.imencode('.jpg', cap.read()[1], (cv.IMWRITE_JPEG_QUALITY, 50))[1][:, 0]
    #frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #frame = cv.resize(frame,(200, 200), interpolation = cv.INTER_CUBIC)
    #buf = bytes(frame.flatten())
    s.sendto(bytes([buf.size % 256, buf.size // 256]), ('192.168.137.1', 2345))
    s.sendto(bytes(buf), ('192.168.137.1', 2345))
