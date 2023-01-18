import os
import numpy as np

# pwd测试
pwd = os.path.split(os.path.realpath(__file__))[0]
print(pwd)

a = np.ones(5)
for i in range(5):
    a[i] = i
print(max(a))