#%% 加载rawdata测试
from email import header
import numpy as np
import pandas as pd

data_save = np.empty(shape=[128, 3])
for LaserID in range(128):
    laser_data_file = '/home/hesai/Project/DistCalibDebug/3号台切入测试验证/正常生产校准数据/AT3BC458973BC45E_userid1_realdist2.10_4.05_8.24_20.08_20.23_single0_threshold0_25_ischeck0_laserpower24_25_128_mode_max_slope/origin_data_pixelid{}.npz'.format(
        LaserID)
    datas = np.load(laser_data_file)

    np.set_printoptions(threshold=np.inf, suppress=True)  # 去掉省略,关闭科学计数法
    # print(datas.files)
    # print('pulse_width_capture shape', datas['pulse_width_capture'].shape)
    # num = 0
    # for i in datas['pulse_width_capture'][1][0]:
    #     if i[0] != -1 and i[0] != 0:
    #         num = num + 1
    #         print(i)
    # print(num)
    # data = datas['pulse_width_capture'][3][2][
    #     datas['pulse_width_capture'][3][2][0] != -1]
    data = np.array(datas['pulse_width_capture'])
    data_dist3_loop2 = data[3, 2, :, 0]
    data_dist4_loop2 = data[4, 2, :, 0]
    # print('data shape', data.shape)
    # print('data_dist3_loop2 size', data_dist3_loop2.shape)
    # print('data_dist4_loop2 size', data_dist4_loop2.shape)
    data_dist3_loop2_valid = data_dist3_loop2[(data_dist3_loop2[:] != -1)
                                              & (data_dist3_loop2[:] != 0)]
    data_dist4_loop2_valid = data_dist4_loop2[(data_dist4_loop2[:] != -1)
                                              & (data_dist4_loop2[:] != 0)]
    print('laserID ', LaserID)
    data_save[LaserID, 0] = len(data_dist3_loop2_valid)
    data_save[LaserID, 1] = len(data_dist4_loop2_valid)
    data_save[LaserID,
              2] = len(data_dist3_loop2_valid) + len(data_dist4_loop2_valid)
    pd_data_save = pd.DataFrame(data_save)
    pd_data_save.to_csv(
        "/home/hesai/Project/DistCalibDebug/Repeat_Test/重复测试分析/board45_data_cnt.csv",
        index=False,
        header=False)

    print('data_dist3_loop2 valid size ', len(data_dist3_loop2_valid))
    print('data_dist4_loop2 valid size ', len(data_dist4_loop2_valid))
    print('*********************************************************')
    # print('data_dist3_loop2 valid', data_dist3_loop2_valid)
    # print('data_dist4_loop2 valid', data_dist4_loop2_valid)

#%% 加载fittingdata测试
import numpy as np

FITTING_FILE_NAME = '/home/wangcong/Documents/工程/AT128距离校准/数据比对/fitting_data_pixelid0.npz'
FittingArray = np.load(FITTING_FILE_NAME)
print(FittingArray.files)
np.set_printoptions(threshold=np.inf, suppress=True)  # 去掉省略,关闭科学计数法

KeyPointx = FittingArray['KeyPointx']
KeyPointy = FittingArray['KeyPointy']
fitting_modify = FittingArray['fitting_modify']
fitting_modify_pure = FittingArray['fitting_modify_pure']
X_pulse = FittingArray['X_pulse']
Y_dist = FittingArray['Y_dist']
fitting_point_single_pixel = FittingArray['fitting_point_single_pixel']

print('KeyPointx维度', KeyPointx.shape)
print('KeyPointy维度', KeyPointy.shape)
print('fitting_modify维度', fitting_modify.shape)
print('fitting_modify_pure维度', fitting_modify_pure.shape)
print('X_pulse维度', X_pulse.shape)
print('Y_dist维度', Y_dist.shape)
print('fitting_point_single_pixel维度', fitting_point_single_pixel.shape)

print('fitting_modify_loop0', fitting_modify[0, 0, :])
print('fitting_modify_loop1', fitting_modify[0, 1, :])
print('fitting_modify_loop2', fitting_modify[0, 2, :])

print('fitting_point_single_pixel_loop0', fitting_point_single_pixel[0, 0, :])
print('fitting_point_single_pixel_loop1', fitting_point_single_pixel[0, 1, :])
print('fitting_point_single_pixel_loop2', fitting_point_single_pixel[0, 2, :])
#%% 加载parameter_global测试
import numpy as np

PARAM_FILE_NAME = '/home/wangcong/Project/FPControl/data_store/AT34C15E9B34C15E_userid0_realdist2.10_4.05_8.24_20.08_20.23_single0_threshold0_25_ischeck0_laserpower24_25_128_mode_max_slope/parameter_global.npz'
ParamArray = np.load(PARAM_FILE_NAME)

print(ParamArray.files)
np.set_printoptions(threshold=np.inf, suppress=True)  # 去掉省略,关闭科学计数法

print('pixel_list', ParamArray['pixel_list'])
print('laser_power_list', ParamArray['laser_power_list'])
print('real_distance_list', ParamArray['real_distance_list'])
print('udp_num', ParamArray['udp_num'])
print('threshold_num', ParamArray['threshold_num'])
print('threshold', ParamArray['threshold'])
print('start_threshold', ParamArray['start_threshold'])
print('is_calibration_check', ParamArray['is_calibration_check'])
print('sipm_hv', ParamArray['sipm_hv'])
print('data_format_id', ParamArray['data_format_id'])
print('parallel_pixel_capture_num', ParamArray['parallel_pixel_capture_num'])
print('logic_version', ParamArray['logic_version'])
print('near_code_list', ParamArray['near_code_list'])
print('real_distance_array', ParamArray['real_distance_array'])
print(type(ParamArray))

pixel_list = ParamArray['pixel_list']
laser_power_list = ParamArray['laser_power_list']
real_distance_list = ParamArray['real_distance_list']
udp_num = ParamArray['udp_num']
threshold_num = ParamArray['threshold_num']
threshold = ParamArray['threshold']
start_threshold = ParamArray['start_threshold']
is_calibration_check = ParamArray['is_calibration_check']
sipm_hv = ParamArray['sipm_hv']
data_format_id = ParamArray['data_format_id']
parallel_pixel_capture_num = ParamArray['parallel_pixel_capture_num']
logic_version = ParamArray['logic_version']
near_code_list = ParamArray['near_code_list']
real_distance_array = ParamArray['real_distance_array']

REAL_DIST_OFFSET = 0.022
real_dist_array_station = np.zeros((5, 2, 8))
real_dist_array_station[1, 0, :] = np.array([
    20.067, 20.065, 20.062, 20.061, 20.061, 20.062, 20.064, 20.067
]) + REAL_DIST_OFFSET
real_dist_array_station[1, 1, :] = np.array([
    8.224, 8.223, 8.221, 8.222, 8.222, 8.222, 8.222, 8.223
]) + REAL_DIST_OFFSET

print('real_distance_array shape', real_distance_array.shape)

real_distance_array[2] = real_dist_array_station[1, 1, :]
real_distance_array[3] = real_dist_array_station[1, 0, :]
real_distance_array[4] = real_dist_array_station[1, 0, :]

print('real_distance_array after modification', real_distance_array)
np.savez('parameter_global.npz',
         pixel_list=ParamArray['pixel_list'],
         laser_power_list=ParamArray['laser_power_list'],
         real_distance_list=ParamArray['real_distance_list'],
         udp_num=ParamArray['udp_num'],
         threshold_num=ParamArray['threshold_num'],
         threshold=ParamArray['threshold'],
         start_threshold=ParamArray['start_threshold'],
         is_calibration_check=ParamArray['is_calibration_check'],
         sipm_hv=ParamArray['sipm_hv'],
         data_format_id=ParamArray['data_format_id'],
         parallel_pixel_capture_num=ParamArray['parallel_pixel_capture_num'],
         logic_version=ParamArray['logic_version'],
         near_code_list=ParamArray['near_code_list'],
         real_distance_array=real_distance_array)