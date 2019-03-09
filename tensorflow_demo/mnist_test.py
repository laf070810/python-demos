import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
import TensorflowTest as tftest

mnist = input_data.read_data_sets(tftest.DATA_PATH, one_hot=True)

with tf.Graph().as_default() as g:
    x = tf.placeholder(tf.float32, [mnist.test.num_examples, tftest.IMAGE_SIZE, tftest.IMAGE_SIZE, tftest.CHANNEL_NUM])
    y_ = tf.placeholder(tf.float32, [None, tftest.OUTPUT_NODE])
    y = tftest.build(x, 0.0001)

    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    saver = tf.train.Saver()
    with tf.Session() as sess:
        ckpt = tf.train.get_checkpoint_state(tftest.MODEL_PATH)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
            global_step = ckpt.model_checkpoint_path.split("/")[-1].split("-")[-1]
            reshaped_xs = np.reshape(mnist.test.images, (mnist.test.num_examples, tftest.IMAGE_SIZE, tftest.IMAGE_SIZE, tftest.CHANNEL_NUM))
            accuracy_score = sess.run(accuracy, feed_dict = {x : reshaped_xs, y_ : mnist.test.labels})
            print("After {} training steps, test accuracy = {}".format(global_step, accuracy_score))
        else:
            print("No checkpoint file found")
