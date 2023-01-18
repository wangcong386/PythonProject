#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import csv

DATAPATH = '/home/wangcong/Documents/工程/AT128距离校准/数据比对/'
LASER_ID = 61
CHNCNT = 128
FITTING_DIST_IDX = 2
FITTING_LOOP_IDX = 2
FITTING_STEPS = 128

# 1. 导入255雷达的指定通道的拟合曲线
fitting_single_curve_255 = np.zeros((2, 128))
fitting_single_chn_255 = np.load(
    DATAPATH + 'fitting_data_pixelid{}_255.npz'.format(LASER_ID))
# print(fitting_single_chn['KeyPointx'].shape)
fitting_single_curve_255[0] = fitting_single_chn_255['KeyPointx'][
    FITTING_DIST_IDX, FITTING_LOOP_IDX]
fitting_single_curve_255[1] = fitting_single_chn_255['KeyPointy'][
    FITTING_DIST_IDX, FITTING_LOOP_IDX]
print('keypoint 255:', fitting_single_curve_255)

# 1. 导入468雷达的指定通道的拟合曲线
fitting_single_curve_468 = np.zeros((2, 128))
fitting_single_chn_468 = np.load(
    DATAPATH + 'fitting_data_pixelid{}_468.npz'.format(LASER_ID))
# print(fitting_single_chn['KeyPointx'].shape)
fitting_single_curve_468[0] = fitting_single_chn_468['KeyPointx'][
    FITTING_DIST_IDX, FITTING_LOOP_IDX]
fitting_single_curve_468[1] = fitting_single_chn_468['KeyPointy'][
    FITTING_DIST_IDX, FITTING_LOOP_IDX]
print('keypoint 468:', fitting_single_curve_468[1])

a = fitting_single_curve_468[1]
b = fitting_single_curve_255[1]
fitting_single_curve_diff = np.subtract(fitting_single_curve_468[1],
                                        fitting_single_curve_255[1])
with open(DATAPATH + 'compare_result.csv', 'a+', newline='') as f:
    diff_writer = csv.writer(f)
    diff_writer.writerow(['keypointx', 'keypointy_255', 'keypointy_468',
                         'keypoint_diff'])
    for idx in range(128):
        diff_writer.writerow([fitting_single_curve_468[0, idx],
                             fitting_single_curve_255[1, idx],
                             fitting_single_curve_468[1, idx],
                             fitting_single_curve_diff[idx]])
