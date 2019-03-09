import numpy as np
X = 6
Y = 6

field = np.array([[0 for _ in range(X)] for _ in range(Y)], np.float64)

for i in range(Y):
    field[i][0] = i + 1

alpha = 0.5
while True:
    for i in range(1, X - 1):
        for j in range(1, Y - 1):
            field[i][j] = field[i][j] + (alpha / 4.0) * (field[i - 1][j] + field[i][j - 1] + field[i + 1][j] + field[i][j + 1] - 4 * field[i][j])
    print(field)
