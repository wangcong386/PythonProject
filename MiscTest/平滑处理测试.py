#%% 测试平滑处理效果，处理一条曲线
import numpy as np
import pandas as pd
import os


def smooth_filter(fitting_points, window_width=5):
    smoothed_points = fitting_points.copy()
    ext_array = np.concatenate(
        (fitting_points[0].repeat(window_width), fitting_points,
         fitting_points[-1].repeat(window_width)))

    for step_id in range(128):
        smoothed_points[step_id] = ext_array[step_id + window_width // 2 +
                                             1:step_id + window_width +
                                             window_width // 2 + 1].mean()

    return smoothed_points


DATAPATH = '/home/wangcong/Documents/工程/AT128距离校准/数据比对/'
DATAOUTPATH = '/home/wangcong/Project/DistCalibDebug/'
FITTING_POINT_ARRAY_FOLDER = "/fitting_y_smoothed"
CHN_IDX = 1
DIST_IDX = 2
LOOP_IDX = 2
distance_artificial_offset = 2
ns2m = 0.1498527
lsb2m = ns2m / 256
m2lsb = 1 / lsb2m
SN = 'AT3CCF55963CCF50'

#判断是否存在文件夹如果不存在则创建为文件夹
OUTPUT_FOLDER = DATAOUTPATH + SN + FITTING_POINT_ARRAY_FOLDER
folder_exists = os.path.exists(OUTPUT_FOLDER)
if not folder_exists:
    os.makedirs(OUTPUT_FOLDER)

origion_data = np.load(
    DATAPATH +
    '{}_userid0_realdist2.10_4.05_8.24_20.08_20.23_single0_threshold0_25_ischeck0_laserpower24_25_128_mode_max_slope/fitting_data_pixelid{}.npz'
    .format(SN, CHN_IDX))
fitting_y = origion_data['fitting_point_single_pixel'][DIST_IDX][LOOP_IDX]
# 单位转换+阈值限制
fitting_y[fitting_y <= 0] = 0x1ffff

fitting_y -= distance_artificial_offset * m2lsb
fitting_y_smoothed = smooth_filter(fitting_y)
fitting_orig_save = pd.DataFrame(fitting_y)
fitting_smoothed_save = pd.DataFrame(fitting_y_smoothed)
fitting_smoothed_save.to_csv(OUTPUT_FOLDER +
                    '/fittingPY_chn{}_dist{}_loop{}_smoothed.csv'.format(
                        CHN_IDX, DIST_IDX, LOOP_IDX),
                    index=False,
                    header=False)
fitting_orig_save.to_csv(OUTPUT_FOLDER +
                    '/fittingPY_chn{}_dist{}_loop{}_orig.csv'.format(
                        CHN_IDX, DIST_IDX, LOOP_IDX),
                    index=False,
                    header=False)

# %%
