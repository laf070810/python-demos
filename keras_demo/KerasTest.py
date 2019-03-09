from keras import regularizers
from keras.models import Sequential, load_model
from keras.layers.core import Dense, Activation, Reshape, Flatten, Dropout
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPooling2D
from keras.optimizers import SGD
from keras.datasets import mnist
import numpy as np

CONV1_SIZE = 5
CONV1_KERNEL_NUM = 32
CONV2_SIZE = 5
CONV2_KERNEL_NUM = 64
MODEL_PATH = "E:/ProgramData/Microsoft Visual Studio/KerasTest/KerasTest/model.h5"

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train[..., np.newaxis]
x_test = x_test[..., np.newaxis]

y_train_reshaped = []
for data in y_train:
    temp = [0 for _ in range(10)]
    temp[data] = 1
    y_train_reshaped.append(temp)
y_train_reshaped = np.array(y_train_reshaped)

y_test_reshaped = []
for data in y_test:
    temp = [0 for _ in range(10)]
    temp[data] = 1
    y_test_reshaped.append(temp)
y_test_reshaped = np.array(y_test_reshaped)

model = Sequential([
    Conv2D(CONV1_KERNEL_NUM, (CONV1_SIZE), activation="relu", padding="SAME", kernel_regularizer=regularizers.l2(0.0001)), 
    MaxPooling2D(pool_size = (2, 2), strides = (2, 2), padding="SAME"), 
    Conv2D(CONV2_KERNEL_NUM, (CONV2_SIZE), activation="relu", padding="SAME", kernel_regularizer=regularizers.l2(0.0001)), 
    MaxPooling2D(pool_size = (2, 2), strides = (2, 2), padding="SAME"), 
    Flatten(),  
    Dense(500, activation="relu", kernel_regularizer=regularizers.l2(0.0001)), 
    Dropout(0.5), 
    Dense(10, activation="softmax", kernel_regularizer=regularizers.l2(0.0001))])
model.compile(optimizer = SGD(lr = 0.1, decay=0.99), loss = "categorical_crossentropy")

#model = load_model(MODEL_PATH)
for i in range(50):
    model.fit(x_train, y_train_reshaped, epochs = 1, batch_size = 500)
    model.save(MODEL_PATH)
model.evaluate(x_test, y_test_reshaped, batch_size = 50)