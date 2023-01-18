#%% 测试测近曲线向右延伸处理效果，处理一条曲线
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import os


def get_fitting_curve_stop_point(curve, is2m=0):
    stop_point_thre = 15
    if is2m == 1:
        for i in range(len(curve) - 2, -1, -1):
            if (curve[i] - curve[-1] > stop_point_thre):
                return i + 1, curve[i + 1]
    else:
        for i in range(len(curve) - 2, -1, -1):
            if (curve[i] == curve[-1]):
                return i + 1, curve[i + 1]


def fitting_curve_right_expand(curve, curve_reference):
    if (len(curve) != 128 or len(curve_reference) != 128):
        print('*******************error empty curve:*****************')
        return curve
    stop_id, stop_value = get_fitting_curve_stop_point(curve, 1)
    stop_id_reference, stop_value_reference = get_fitting_curve_stop_point(
        curve_reference, 0)
    print("stop_id_reference", stop_id_reference)
    plt.plot(curve, 'r*')
    plt.plot(curve_reference, 'g*')
    if (stop_id >= stop_id_reference):
        return curve

    linear_fit_num = 10
    p1 = np.polyfit(np.arange(stop_id - linear_fit_num + 1, stop_id + 1),
                    curve[stop_id - linear_fit_num + 1:stop_id + 1], 1)
    curve[stop_id:stop_id_reference] = np.polyval(
        p1, np.arange(stop_id, stop_id_reference))
    print("curve after polyval", curve)
    curve[stop_id_reference:] = curve[stop_id_reference - 1]
    print("curve after polyval 2", curve)
    if (curve[-1] < stop_value_reference):
        curve[curve < stop_value_reference] = stop_value_reference
    plt.plot(curve, 'b*')
    plt.show()
    return curve


DATAPATH = '/home/wangcong/Documents/工程/AT128距离校准/数据比对/'
DATAOUTPATH = '/home/wangcong/Project/DistCalibDebug/'
FITTING_POINT_ARRAY_FOLDER = "/expand_right"
CHN_IDX = 2
DIST_IDX = 0
DIST_IDX_REF = 1
LOOP_IDX = 1
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
fitting_y_ref = origion_data['fitting_point_single_pixel'][DIST_IDX_REF][
    LOOP_IDX]
fitting_y = origion_data['fitting_point_single_pixel'][DIST_IDX][LOOP_IDX]
# 单位转换+阈值限制
fitting_y_ref[fitting_y_ref <= 0] = 0x1ffff
fitting_y[fitting_y <= 0] = 0x1ffff

fitting_y_ref -= distance_artificial_offset * m2lsb
fitting_y -= distance_artificial_offset * m2lsb

fitting_curve_right_expand(fitting_y, fitting_y_ref)

# fitting_orig_save = pd.DataFrame(fitting_y)
# fitting_smoothed_save = pd.DataFrame(fitting_y_smoothed)
# fitting_smoothed_save.to_csv(
#     OUTPUT_FOLDER + '/fittingPY_chn{}_dist{}_loop{}_smoothed.csv'.format(
#         CHN_IDX, DIST_IDX, LOOP_IDX),
#     index=False,
#     header=False)
# fitting_orig_save.to_csv(OUTPUT_FOLDER +
#                          '/fittingPY_chn{}_dist{}_loop{}_orig.csv'.format(
#                              CHN_IDX, DIST_IDX, LOOP_IDX),
#                          index=False,
#                          header=False)

# %%
