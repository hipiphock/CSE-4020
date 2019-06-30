import numpy as np, OpenGL, glfw

# problem A
M = np.arange(2, 27, 1)
print(M)

# problem B
M = M.reshape(5, 5)
print(M)

# problem C
M[:, 0] = 0
print(M)

# problem D
M = M @ M
print(M)

# problem E
v = M[0]
print(np.sqrt(v @ v))