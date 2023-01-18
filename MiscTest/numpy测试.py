#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

# %% zeros 测试
import numpy as np

testArr = np.zeros([3, 3, 3], np.uint32)
print(testArr[0, :, :].reshape(-1))

# %% concatenate测试
import numpy as np

arr = np.array([0, 1, 2, 3, 4])
print(arr[0:2])
print(np.concatenate((arr[0].repeat(4), arr, arr[-1].repeat(4))))

# %% arange测试
import numpy as np

arr = np.arange(0, 8)+10
arr_need_idx = [1, 2, 3]
print(arr[arr_need_idx])

# %%
