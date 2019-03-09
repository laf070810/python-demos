import cv2 as cv
import socket
import numpy as np
import threading

cap = cv.VideoCapture(0)

def image_tranfer(client):
    global cap
    while True:
        buf = cv.imencode('.jpg', cap.read()[1], (cv.IMWRITE_JPEG_QUALITY, 50))[1][:, 0]
        client.send(bytes([buf.size % 256, buf.size // 256]))
        client.send(bytes(buf))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('www.lianfeng.ml', 3100))
s.listen(5)

while True: 
    client, addr = s.accept()
    print('Connection from ' + str(addr))
    threading.Thread(target=image_tranfer, args=(client, ), daemon=True).start()
