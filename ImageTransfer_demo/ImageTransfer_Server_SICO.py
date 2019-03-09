import cv2 as cv
import socket
import numpy as np

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('192.168.137.1', 2345))

while True:
    try:
        len, addr = s.recvfrom(2)
        data, addr = s.recvfrom(int.from_bytes(len, byteorder='little'))
        buf = np.array(list(data), dtype=np.uint8)
        frame = cv.imdecode(buf, cv.IMREAD_UNCHANGED)
        if frame is not None:
            cv.imshow('', frame)
            cv.waitKey(10)
    except Exception as e:
        print(e)
