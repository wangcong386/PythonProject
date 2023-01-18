
import numpy as np
import os
import csv


for channel_index in range(128):
    singleChannel = [[]]
    with open("/home/wangcong/Documents/test/{}.csv".format(channel_index),"w") as csvfile:
        writer = csv.writer(csvfile)
        file_fitting_chong = '/home/wangcong/Downloads/machine164_userid0_realdist2.10_4.05_8.24_20.08_single0_threshold0_20_ischeck0_laserpower24_25_128_mode_max_slope/fitting_data_pixelid{}.npz'.format(channel_index)
        file_fitting_me = '/home/wangcong/Projects/FPControl/data_store/machine103_userid0_realdist2.10_4.05_8.24_20.08_single0_threshold0_20_ischeck0_laserpower24_25_128_mode_max_slope/fitting_data_pixelid{}.npz'.format(channel_index)
        if(os.path.exists(file_fitting_chong) and os.path.exists(file_fitting_me)):
            fitting_data_chong = np.load(file_fitting_chong)
            fitting_data_me = np.load(file_fitting_me)
            for board in range(4):
                for loop in range(3):
                    singleLoopArray=[]
                    for ele in range(len(fitting_data_chong['KeyPointy'][board][loop])):
                        if(fitting_data_chong['KeyPointy'][board][loop][ele] and fitting_data_me['KeyPointy'][board][loop][ele]):
                            singleLoopArray.append((fitting_data_chong['KeyPointy'][board][loop][ele] - fitting_data_me['KeyPointy'][board][loop][ele])*100)
                    singleChannel.append(singleLoopArray)
                    writer.writerow(singleLoopArray)
        csvfile.close

