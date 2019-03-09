from filterpy.kalman import KalmanFilter
import numpy as np

T = 0.1
f = KalmanFilter(dim_x = 3, dim_z = 3)
f.x = np.array([0.0, 0.0, 0.0])
f.F = np.array([[1, T, 0.5 * T ** 2], [0, 1, T], [0, 0, 1]])
f.H = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
f.P = np.array([[0.1, 0, 0], [0, 0.1, 0], [0, 0, 0.1]])
f.R = np.array([[2, 0, 0], [0, 2, 0], [0, 0, 2]])
f.Q = np.array([[0.2, 0, 0], [0, 0.2, 0], [0, 0, 0.2]])

file = open("E:\\ProgramData\\MATLAB\\test.dat", 'r')
for line in file:
    f.predict()
    f.update(np.array(line.split(" ")[0:3], dtype = 'float64'))
    print(str(f.x) + "\n")