#import sys
#from PyQt5.QtWidgets import QApplication, QMainWindow
#from PyQt5.uic import loadUiType
#from PyQt5.QtCore import Qt

#class_ui, class_base = loadUiType("pc2.ui")
#class Example(class_ui, class_base):

#    def __init__(self):
#        super().__init__()
#        self.setupUi(self)
#        self.setWindowTitle("Demo")
#        self.showMaximized()

#app = QApplication(sys.argv)
#a = Example();
#sys.exit(app.exec_())

import tensorflow as tf
import numpy as np

BATCH_SIZE = 8
seed = 23455

rng = np.random.RandomState(seed)
X = rng.rand(32, 2)
Y = [[int(x0 + x1 < 1)] for (x0, x1) in X]
print ("X:\n{}".format(X))
print ("Y:\n{}".format(Y))
x = tf.placeholder(tf.float32, shape = (None, 2))
y_ = tf.placeholder(tf.float32, shape = (None, 1))
w1 = tf.Variable(tf.random_normal([2, 3], stddev = 1, seed = 1))
w2 = tf.Variable(tf.random_normal([3, 1], stddev = 1, seed = 1))
a = tf.matmul(x, w1)
y = tf.matmul(a, w2)
loss = tf.reduce_mean(tf.square(y - y_))
train_step = tf.train.GradientDescentOptimizer(0.001).minimize(loss)
with tf.Session() as sess:
    init_op = tf.global_variables_initializer()
    sess.run(init_op)
    print("w1:\n{}".format(sess.run(w1)))
    print("w2:\n{}".format(sess.run(w2)))
    print("\n")

    STEPS = 50000
    for i in range(STEPS):
        start = (i * BATCH_SIZE) % 32
        end = start + BATCH_SIZE
        sess.run(train_step, feed_dict = {x : X[start:end], y_ : Y[start:end]})
        if i % 500 == 0:
            total_loss = sess.run(loss, feed_dict = {x : X, y_ : Y})
            print("After {} trainging steps, loss on all data is {}".format(i, total_loss))

    print("\n")
    print("w1:\n{}".format(sess.run(w1)))
    print("w2:\n{}".format(sess.run(w2)))

#命令：python "E:\ProgramData\Microsoft Visual Studio\PythonTest\PythonTest\PythonTest.py"

