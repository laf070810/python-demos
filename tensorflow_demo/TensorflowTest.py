import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data

INPUT_NODE = 784
OUTPUT_NODE = 10
LAYER1_NODE = 500
BATCH_SIZE = 200
STEPS = 50000
REGULARIZER = 0.0001

DATA_PATH = "E:/ProgramData/Microsoft Visual Studio/MNIST"
MODEL_PATH = "./model/"
MODEL_NAME = "mnist_model"
IMAGE_SIZE = 28
CHANNEL_NUM = 1

CONV1_SIZE = 5
CONV1_KERNEL_NUM = 32
CONV2_SIZE = 5
CONV2_KERNEL_NUM = 64

def generateds():
    rdm = np.random.RandomState(1)
    X = rdm.rand(32, 2)
    Y_ = [[x1 + x2 + rdm.rand()/10.0 - 0.05] for (x1, x2) in X]
    return X, Y_

def build(x, regularizer):
    conv1_w = tf.Variable(tf.truncated_normal([CONV1_SIZE, CONV1_SIZE, CHANNEL_NUM, CONV1_KERNEL_NUM], stddev = 0.1))
    tf.add_to_collection("losses", tf.contrib.layers.l2_regularizer(regularizer)(conv1_w))
    conv1_b = tf.Variable(tf.zeros([CONV1_KERNEL_NUM]))
    relu1 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(x, conv1_w, strides=[1, 1, 1, 1], padding = "SAME"), conv1_b))
    pool1 = tf.nn.max_pool(relu1, ksize=[1, 2, 2, 1], strides = [1, 2, 2, 1], padding = "SAME")

    conv2_w = tf.Variable(tf.truncated_normal([CONV2_SIZE, CONV2_SIZE, CHANNEL_NUM, CONV2_KERNEL_NUM], stddev = 0.1))
    tf.add_to_collection("losses", tf.contrib.layers.l2_regularizer(regularizer)(conv2_w))
    conv2_b = tf.Variable(tf.zeros([CONV2_KERNEL_NUM]))
    relu2 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(x, conv2_w, strides=[1, 1, 1, 1], padding = "SAME"), conv2_b))
    pool2 = tf.nn.max_pool(relu2, ksize=[1, 2, 2, 1], strides = [1, 2, 2, 1], padding = "SAME")

    pool_shape = pool2.get_shape().as_list()
    nodes = pool_shape[1] * pool_shape[2] * pool_shape[3]
    reshaped = tf.reshape(pool2, [pool_shape[0], nodes])

    w1 = tf.Variable(tf.truncated_normal([nodes, LAYER1_NODE], stddev=0.1))
    tf.add_to_collection("losses", tf.contrib.layers.l2_regularizer(regularizer)(w1))
    b1 = tf.Variable(tf.zeros([LAYER1_NODE]))
    y1 = tf.nn.relu(tf.matmul(reshaped, w1) + b1)
    if train:
        y1 = tf.nn.dropout(y1, 0.5)

    w2 = tf.Variable(tf.truncated_normal([LAYER1_NODE, OUTPUT_NODE], stddev=0.1))
    tf.add_to_collection("losses", tf.contrib.layers.l2_regularizer(regularizer)(w2))
    b2 = tf.Variable(tf.zeros([OUTPUT_NODE]))
    y = tf.matmul(y1, w2) + b2

    return y

def train():
    x = tf.placeholder(tf.float32, shape = [BATCH_SIZE, IMAGE_SIZE, IMAGE_SIZE, CHANNEL_NUM])
    y_ = tf.placeholder(tf.float32, shape = (None, OUTPUT_NODE))
    y = build(x, REGULARIZER)

    global_step = tf.Variable(0, trainable=False)
    loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits = y, labels = tf.argmax(y_, 1))) + tf.add_n(tf.get_collection("losses"))
    learning_rate = tf.train.exponential_decay(0.1, 1, global_step, 0.99, staircase=True)
    train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)

    saver = tf.train.Saver()
    with tf.Session() as sess:
        init_op = tf.global_variables_initializer()
        sess.run(init_op)

        ckpt = tf.train.get_checkpoint_state(MODEL_PATH)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)

        for i in range(STEPS):
            xs, ys = mnist.train.next_batch(BATCH_SIZE)
            reshaped_xs = np.reshape(xs, (BATCH_SIZE, IMAGE_SIZE, IMAGE_SIZE, CHANNEL_NUM))
            _, loss_value, step = sess.run([train_step, loss, global_step], feed_dict = {x : reshaped_xs, y_ : ys})
            if i % 100 == 0:
                print("After {} training steps, loss on the training batch is: {}".format(step, loss_value))
                saver.save(sess, MODEL_PATH + MODEL_NAME, global_step = global_step)

if __name__ == "__main__":
    mnist = input_data.read_data_sets(DATA_PATH, one_hot=True)
    train()
