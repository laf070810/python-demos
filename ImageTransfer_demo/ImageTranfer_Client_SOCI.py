import cv2 as cv
import socket
import numpy as np

def recv_wrapper(socket, length):
    buf = socket.recv(length)
    while len(buf) < length:
        buf += (socket.recv(length - len(buf)))
    return buf

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('www.lianfeng.ml', 3100))

while True:
    try: 
        length = int.from_bytes(recv_wrapper(s, 2), byteorder='little')
        data = recv_wrapper(s, length)
        buf = np.array(list(data), dtype=np.uint8)
        frame = cv.imdecode(buf, cv.IMREAD_UNCHANGED)
        if frame is not None:
            cv.imshow('', frame)
            cv.waitKey(10)
    except Exception as e: 
        print(e)
