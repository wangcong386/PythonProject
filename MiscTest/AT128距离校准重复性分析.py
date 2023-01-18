#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

DATAPATH = '/home/wangcong/Downloads/'
LIDARCNT = 1
CHNCNT = 128
FITTINGDIM = 2
FITTINGDIM0 = 0
FITTINGDIM1 = 1
FITTINGDISTCNT = 4
FITTINGLOOPCNT = 3
FITTINGSTEPS = 128
STATISTIC_STEP = 3  # 指定通道、距离、光强下的数据分析：0=最小值 1=最大值 2=差值
# todo:
# 1. 导入25台雷达的所有通道的拟合曲线
fitting_all_lidar = np.zeros((LIDARCNT, CHNCNT, FITTINGDIM, FITTINGDISTCNT,
                              FITTINGLOOPCNT, FITTINGSTEPS))
# print(fitting_all_lidar.shape)
for lidar_idx in range(LIDARCNT):
    for chn_idx in range(CHNCNT):
        fitting_single_chn = np.load(
            DATAPATH +
            'machine164_userid{}_realdist2.10_4.05_8.24_20.08_single0_threshold0_20_ischeck0_laserpower24_25_128_mode_max_slope/fitting_data_pixelid{}.npz'
            .format(lidar_idx, chn_idx))
        # print(fitting_single_chn['KeyPointx'].shape)
        fitting_all_lidar[lidar_idx, chn_idx,
                          FITTINGDIM0] = fitting_single_chn['KeyPointx']
        fitting_all_lidar[lidar_idx, chn_idx,
                          FITTINGDIM1] = fitting_single_chn['KeyPointy']
# print(fitting_all_lidar[0][127][0])

# 2. 横轴所有值都一样，横向对比纵坐标，同通道、距离、光强下曲线各个STEP的最大、最小、差值
fitting_all_lidar_Y_single_step_diff = np.zeros(
    (CHNCNT, FITTINGDISTCNT, FITTINGLOOPCNT, FITTINGSTEPS, STATISTIC_STEP))
for chn_idx in range(CHNCNT):
    for dist_idx in range(FITTINGDISTCNT):
        for loop_idx in range(FITTINGLOOPCNT):
            for fitting_step in range(FITTINGSTEPS):
                # for lidar_idx in range(LIDARCNT):
                static_single_line = fitting_all_lidar[:, chn_idx, FITTINGDIM1,
                                                       dist_idx, loop_idx,
                                                       fitting_step]
                # print(static_single_line.shape)
                fitting_all_lidar_Y_single_step_diff[
                    chn_idx, dist_idx, loop_idx, fitting_step,
                    0] = static_single_line.min()
                fitting_all_lidar_Y_single_step_diff[
                    chn_idx, dist_idx, loop_idx, fitting_step,
                    1] = static_single_line.max()
                fitting_all_lidar_Y_single_step_diff[
                    chn_idx, dist_idx, loop_idx, fitting_step,
                    2] = static_single_line.max() - static_single_line.min()
print(fitting_all_lidar_Y_single_step_diff)

# 2. 同通道、距离、光强下每条曲线所有STEP差值的最小、最大值
STATISTIC_CURVE = 2
fitting_all_lidar_Y_single_curve_diff = np.zeros(
    (CHNCNT, FITTINGDISTCNT, FITTINGLOOPCNT, STATISTIC_CURVE))
for chn_idx in range(CHNCNT):
    for dist_idx in range(FITTINGDISTCNT):
        for loop_idx in range(FITTINGLOOPCNT):
            fitting_all_lidar_Y_single_curve_diff[
                chn_idx, dist_idx, loop_idx,
                0] = fitting_all_lidar_Y_single_step_diff[chn_idx, dist_idx,
                                                          loop_idx, :,
                                                          2].min()
            fitting_all_lidar_Y_single_curve_diff[
                chn_idx, dist_idx, loop_idx,
                1] = fitting_all_lidar_Y_single_step_diff[chn_idx, dist_idx,
                                                          loop_idx, :,
                                                          2].max()
print(fitting_all_lidar_Y_single_curve_diff)

# # 3. 同通道、距离下所有loop曲线差异的最小、最大值
# fitting_all_lidar_Y_single_loop_diff = np.zeros(
#     (CHNCNT, FITTINGDISTCNT, STATISTIC_CURVE))
# for chn_idx in range(CHNCNT):
#     for dist_idx in range(FITTINGDISTCNT):
#         fitting_all_lidar_Y_single_loop_diff[chn_idx,dist_idx,0]=fitting_all_lidar_Y_single_curve_diff[
#                 chn_idx, dist_idx,:,0].min
