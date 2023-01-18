#%% 测试各种运算符

val_1 = 14 // 3
print('val_1', val_1)

val_2 = 100 // 2**3
print('val_2', val_2)

val_2_0 = -100 // 2**3
print('val_2_0', val_2_0)

val_3 = 100 % 3
print('val_3', val_3)

val_4 = 100 / 3
print('val_4', val_4)

# += 测试

val_5 = 2
val_5 += 1
print('val_5', val_5)
# %% numpy 测试

import numpy as np

arr_test1 = np.zeros([1, 3], dtype=float)
arr_test1[0, 0] = -0x1ffff
arr_test1[0, 1] = -0x1ffff * 2
arr_test1[0, 2] = -0x1ffff * 3
print(arr_test1)
arr_test2 = arr_test1.astype(np.uint32)
print(arr_test2)

# %% 小测试

val_little_test = (1023 // 8) * (2**0 + 2**8 + 2**16 + 2**24)
print('val_little_test{:0>8x}'.format(int(val_little_test)))

# %% 多变量for循环测试
xlist = [0, 1, 2, 3, 4]
ylist = [11, 12, 13]
for x, y in zip(xlist, ylist):
    print(x, y)

# %%
