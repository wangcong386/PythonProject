#%%
# 1.导出原始数据，存入csv表格，只保存有效数据

import numpy as np
import pandas as pd
import sqlite3

from 加载数据测试 import FITTING_FILE_NAME

DATAPATH = '/home/wangcong/Documents/工程/AT128距离校准/数据比对/'
CHN_CNT = 128
DIST_CNT = 4
LOOP_CNT = 3

for chn_idx in range(CHN_CNT):
    origion_data = np.load(
        DATAPATH +
        'AT128-HB2LX-0014_userid33_realdist2.10_4.05_8.24_20.08_20.23_single0_threshold0_25_ischeck0_laserpower24_25_128_mode_max_slope/fitting_data_pixelid{}.npz'
        .format(chn_idx))
    for dist_idx in range(DIST_CNT):
        for loop_idx in range(LOOP_CNT):
            data_valid_idx = np.argwhere(
                origion_data['X_pulse'][dist_idx][loop_idx] != 0)
            if len(data_valid_idx) == 0:
                continue
            else:
                data_raw_x_valid = origion_data['X_pulse'][dist_idx][loop_idx][
                    data_valid_idx]
                data_raw_y_valid = origion_data['Y_dist'][dist_idx][loop_idx][
                    data_valid_idx]
                data_both = np.zeros((len(data_raw_x_valid), 2))
                data_both[:, 0] = data_raw_x_valid[:, 0]
                data_both[:, 1] = data_raw_y_valid[:, 0]
                data_save = pd.DataFrame(data_both)
                data_save.to_csv(
                    DATAPATH +
                    '/DataTransform/rawdata_chn{}_dist{}_loop{}.csv'.format(
                        chn_idx, dist_idx, loop_idx),
                    index=False,
                    header=False)

                fitting_x = origion_data['KeyPointx'][dist_idx][loop_idx]
                fitting_y = origion_data['fitting_modify'][dist_idx][loop_idx]
                # print(fitting_x)
                fitting_both = np.zeros((len(fitting_x), 2))
                fitting_both[:, 0] = fitting_x[:]
                fitting_both[:, 1] = fitting_y[:]
                fitting_save = pd.DataFrame(fitting_both)
                fitting_save.to_csv(
                    DATAPATH +
                    '/DataTransform/fittingPY_chn{}_dist{}_loop{}.csv'.format(
                        chn_idx, dist_idx, loop_idx),
                    index=False,
                    header=False)
#%% 2.导出拟合数据存入csv表格，保存所有数据

import numpy as np
import pandas as pd
import sqlite3
import os

DATAPATH = '/home/wangcong/Documents/工程/AT128距离校准/数据比对/'
DATAOUTPATH = '/home/wangcong/Project/DistCalibDebug/'
FITTING_POINT_ARRAY_FOLDER = "/fitting_point_array"
CHN_CNT = 128
DIST_CNT = 5
LOOP_CNT = 3
SN = 'AT3CCF55963CCF50'

#判断是否存在文件夹如果不存在则创建为文件夹
OUTPUT_FOLDER = DATAOUTPATH + SN + FITTING_POINT_ARRAY_FOLDER
folder_exists = os.path.exists(OUTPUT_FOLDER)
if not folder_exists:
    os.makedirs(OUTPUT_FOLDER)

for chn_idx in range(CHN_CNT):
    origion_data = np.load(
        DATAPATH +
        '{}_userid0_realdist2.10_4.05_8.24_20.08_20.23_single0_threshold0_25_ischeck0_laserpower24_25_128_mode_max_slope/fitting_data_pixelid{}.npz'
        .format(SN, chn_idx))
    for dist_idx in range(DIST_CNT):
        for loop_idx in range(LOOP_CNT):
            fitting_x = origion_data['KeyPointx'][dist_idx][loop_idx]
            fitting_y = origion_data['fitting_point_single_pixel'][dist_idx][
                loop_idx]
            # print(fitting_x)
            fitting_both = np.zeros((len(fitting_x), 2))
            fitting_both[:, 0] = fitting_x[:]
            fitting_both[:, 1] = fitting_y[:]
            fitting_save = pd.DataFrame(fitting_both)
            fitting_save.to_csv(OUTPUT_FOLDER +
                                '/fittingPY_chn{}_dist{}_loop{}.csv'.format(
                                    chn_idx, dist_idx, loop_idx),
                                index=False,
                                header=False)
#%% 3.导出processed_global数据
import numpy as np
import pandas as pd

DATAPATH = '/home/wangcong/Documents/工程/AT128距离校准/数据比对/'
DATAOUTPATH = '/home/wangcong/Project/DistCalibDebug/'
CHN_CNT = 128
DIST_CNT = 5
LOOP_CNT = 3
SN = 'AT3CCF55963CCF50'

processedArray = np.load(
    DATAPATH +
    '{}_userid0_realdist2.10_4.05_8.24_20.08_20.23_single0_threshold0_25_ischeck0_laserpower24_25_128_mode_max_slope/processed_global.npz'
    .format(SN))
print(processedArray.files)
np.set_printoptions(threshold=np.inf, suppress=True)  # 去掉省略,关闭科学计数法

fitting_point_array = processedArray['fitting_point_array']
dist2_fitting_point_array = processedArray['dist2_fitting_point_array']
fitting_point_array_mean = processedArray['fitting_point_array_mean']

print('fitting_point_array维度', fitting_point_array.shape)
print('dist2_fitting_point_array维度', dist2_fitting_point_array.shape)
print('fitting_point_array_mean维度', fitting_point_array_mean.shape)

# print('fitting_point_array', fitting_point_array[2, :, 2, :])
# print('dist2_fitting_point_array', dist2_fitting_point_array[0, :, 1, :])

for chn_idx in range(CHN_CNT):
    for dist_idx in range(DIST_CNT):
        for loop_idx in range(LOOP_CNT):
            fitting_x = fitting_point_array[chn_idx][dist_idx][loop_idx]
            fitting_y = fitting_point_array[chn_idx][dist_idx][loop_idx]
            fitting_y_dist2 = dist2_fitting_point_array[chn_idx][dist_idx][
                loop_idx]
            fitting_three = np.zeros((len(fitting_x), 3))
            fitting_three[:, 0] = fitting_x[:]
            fitting_three[:, 1] = fitting_y[:]
            fitting_three[:, 2] = fitting_y_dist2[:]
            fitting_save = pd.DataFrame(fitting_three)
            fitting_save.to_csv(DATAOUTPATH +
                                '/fittingPY_chn{}_dist{}_loop{}.csv'.format(
                                    chn_idx, dist_idx, loop_idx),
                                index=False,
                                header=False)
#%% 4.导出processed_global数据+拟合数据
import numpy as np
import pandas as pd

DATAPATH = '/home/wangcong/Documents/工程/AT128距离校准/数据比对/'
DATAOUTPATH = '/home/wangcong/Project/DistCalibDebug/'
FITTING_POINT_ARRAY_FOLDER = "/fitting_point_array"
CHN_CNT = 128
DIST_CNT = 5
LOOP_CNT = 3
SN = 'AT3CCF55963CCF50'

processedArray = np.load(
    DATAPATH +
    '{}_userid0_realdist2.10_4.05_8.24_20.08_20.23_single0_threshold0_25_ischeck0_laserpower24_25_128_mode_max_slope/processed_global.npz'
    .format(SN))
print(processedArray.files)
np.set_printoptions(threshold=np.inf, suppress=True)  # 去掉省略,关闭科学计数法

fitting_point_array = processedArray['fitting_point_array']
dist2_fitting_point_array = processedArray['dist2_fitting_point_array']
fitting_point_array_mean = processedArray['fitting_point_array_mean']

print('fitting_point_array维度', fitting_point_array.shape)
print('dist2_fitting_point_array维度', dist2_fitting_point_array.shape)
print('fitting_point_array_mean维度', fitting_point_array_mean.shape)

#判断是否存在文件夹如果不存在则创建为文件夹
OUTPUT_FOLDER = DATAOUTPATH + SN + FITTING_POINT_ARRAY_FOLDER
folder_exists = os.path.exists(OUTPUT_FOLDER)
if not folder_exists:
    os.makedirs(OUTPUT_FOLDER)

for chn_idx in range(CHN_CNT):
    origion_data = np.load(
        DATAPATH +
        '{}_userid0_realdist2.10_4.05_8.24_20.08_20.23_single0_threshold0_25_ischeck0_laserpower24_25_128_mode_max_slope/fitting_data_pixelid{}.npz'
        .format(SN, chn_idx))
    for dist_idx in range(DIST_CNT):
        for loop_idx in range(LOOP_CNT):
            fitting_x = origion_data['KeyPointx'][dist_idx][loop_idx]
            fitting_y = origion_data['fitting_point_single_pixel'][dist_idx][
                loop_idx]
            fitting_y_modified = fitting_point_array[chn_idx][dist_idx][
                loop_idx]
            fitting_three = np.zeros((len(fitting_x), 3))
            fitting_three[:, 0] = fitting_x[:]
            fitting_three[:, 1] = fitting_y[:]
            fitting_three[:, 2] = fitting_y_modified[:]
            fitting_save = pd.DataFrame(fitting_three)
            fitting_save.to_csv(OUTPUT_FOLDER +
                                '/fittingPY_chn{}_dist{}_loop{}.csv'.format(
                                    chn_idx, dist_idx, loop_idx),
                                index=False,
                                header=False)
# %%
