import numpy as np
import csv

laser_power_list = [24, 25, 128]

pixel_array = []
pixel_array.append([list(range(0,0+16,2)),list(range(17,17+16,2)),list(range(32,32+16,2)),list(range(49,49+16,2)),\
    list(range(64,64+16,2)),list(range(81,81+16,2)),list(range(96,96+16,2)),list(range(113,113+16,2))])
pixel_array.append([list(range(1,1+16,2)),list(range(16,16+16,2)),list(range(33,33+16,2)),list(range(48,48+16,2)),\
    list(range(65,65+16,2)),list(range(80,80+16,2)),list(range(97,97+16,2)),list(range(112,112+16,2))])
pixel_array = np.array(pixel_array)

pixel_list = \
list(range(0,0+16,2))+list(range(17,17+16,2))+list(range(32,32+16,2))+list(range(49,49+16,2))+\
list(range(64,64+16,2))+list(range(81,81+16,2))+list(range(96,96+16,2))+list(range(113,113+16,2))+\
list(range(126,126-16,-2))+list(range(111,111-16,-2))+list(range(94,94-16,-2))+list(range(79,79-16,-2))+\
list(range(62,62-16,-2))+list(range(47,47-16,-2))+list(range(30,30-16,-2))+list(range(15,15-16,-2))

print("pixel_list:", pixel_list)
print("pixel_list:", pixel_list[0::4])

parallel_pixel_capture_num = 8

liangbo_map = [
    17, 16, 19, 18, 21, 20, 23, 22, 25, 24, 27, 26, 29, 28, 31, 30, 1, 0, 3, 2,
    5, 4, 7, 6, 9, 8, 11, 10, 13, 12, 15, 14, 49, 48, 51, 50, 53, 52, 55, 54,
    57, 56, 59, 58, 61, 60, 63, 62, 33, 32, 35, 34, 37, 36, 39, 38, 41, 40, 43,
    42, 45, 44, 47, 46, 81, 80, 83, 82, 85, 84, 87, 86, 89, 88, 91, 90, 93, 92,
    95, 94, 65, 64, 67, 66, 69, 68, 71, 70, 73, 72, 75, 74, 77, 76, 79, 78,
    113, 112, 115, 114, 117, 116, 119, 118, 121, 120, 123, 122, 125, 124, 127,
    126, 97, 96, 99, 98, 101, 100, 103, 102, 105, 104, 107, 106, 109, 108, 111,
    110
]


def get_liangbomap(pixel_addr=[]):
    liangbomap_list = []
    for tmp in pixel_addr:
        liangbomap_list.append(liangbo_map[tmp])
    return liangbomap_list


def get_surround_pixels(pixel_id):
    surround_pixels = []
    pass_num = 4
    pos = np.argwhere(pixel_array == pixel_id)[0]
    if (pos[0] == 0):
        surround_pixels += list(pixel_array[1, pos[1], :])
    elif (pos[0] == 1):
        surround_pixels += list(pixel_array[0, pos[1], :])

    if (pos[1] == 0):
        surround_pixels += list(pixel_array[0, pos[1] + 1, 0:pass_num])
        surround_pixels += list(pixel_array[1, pos[1] + 1, 0:pass_num])
    elif (pos[1] == 7):
        surround_pixels += list(pixel_array[0, pos[1] - 1, 8 - pass_num:])
        surround_pixels += list(pixel_array[1, pos[1] - 1, 8 - pass_num:])
    else:
        surround_pixels += list(pixel_array[0, pos[1] - 1, 8 - pass_num:])
        surround_pixels += list(pixel_array[1, pos[1] - 1, 8 - pass_num:])
        surround_pixels += list(pixel_array[0, pos[1] + 1, 0:pass_num])
        surround_pixels += list(pixel_array[1, pos[1] + 1, 0:pass_num])

    return surround_pixels


def set_laser_power_control(capture_id, pixel_addr=[]):
    pixel_mask_array = np.ones([128, 3])
    for i in range(len(laser_power_list)):
        if (laser_power_list[i] == 24):
            a_set = set(range(128))
            b_set = set(get_surround_pixels(pixel_addr[0]))
            # c_set = set(get_liangbomap(pixel_addr))
            c_set = set()

            open_list = list((a_set - b_set) | c_set)
            pixel_mask_array[:, i] = 0
            pixel_mask_array[open_list, i] = 1
        elif (laser_power_list[i] == 128):
            pixel_addr_temp = pixel_addr.copy()
            # for tmp in pixel_addr:
            #     pixel_addr_temp.append(liangbo_map[tmp])

            pixel_mask_array[:, i] = 0
            pixel_mask_array[pixel_addr_temp, i] = 1
        elif (laser_power_list[i] == 25):
            pixel_mask_array[:, i] = 0
            pixel_mask_array[pixel_addr, i] = 1

    print('pixel_addr', pixel_addr)
    with open('/home/wangcong/Projects/temp/chn_mask_group{}.csv'.format(
            capture_id),
              'a+',
              newline='') as f:
        pixel_mask_writer = csv.writer(f)
        pixel_mask_writer.writerow([
            'LaserMaskG{}L0'.format(capture_id),
            'LaserMaskG{}LN'.format(capture_id),
            'LaserMaskG{}L1'.format(capture_id)
        ])
        for pixel_mask in pixel_mask_array:
            pixel_mask_writer.writerow(
                [pixel_mask[0], pixel_mask[1], pixel_mask[2]])
            print(pixel_mask[0], '/', pixel_mask[1], '/', pixel_mask[2])
    f.close()
    # print('pixel_mask_array:Loop0')
    # for pixel_mask in pixel_mask_array:
    #     print(pixel_mask[0])
    # print('pixel_mask_array:LoopNear')
    # for pixel_mask in pixel_mask_array:
    #     print(pixel_mask[1])
    # print('pixel_mask_array:Loop1')
    # for pixel_mask in pixel_mask_array:
    #     print(pixel_mask[2])


if __name__ == '__main__':
    for capture_id in range(16):
        pixel_addr = pixel_list[capture_id *
                                parallel_pixel_capture_num:capture_id *
                                parallel_pixel_capture_num +
                                parallel_pixel_capture_num]
        print(pixel_addr)
        set_laser_power_control(capture_id, pixel_addr)
    # pixel_addr=[0, 2, 4, 6, 8, 10, 12, 14]
    # pixel_addr=[17, 19, 21, 23, 25, 27, 29, 31]
    # pixel_addr=[32, 34, 36, 38, 40, 42, 44, 46]
    # pixel_addr=[49, 51, 53, 55, 57, 59, 61, 63]
    # pixel_addr=[64, 66, 68, 70, 72, 74, 76, 78]
    # pixel_addr=[81, 83, 85, 87, 89, 91, 93, 95]
    # pixel_addr=[96, 98, 100, 102, 104, 106, 108, 110]
    # pixel_addr=[113, 115, 117, 119, 121, 123, 125, 127]
    # pixel_addr=[126, 124, 122, 120, 118, 116, 114, 112]
    # pixel_addr=[111, 109, 107, 105, 103, 101, 99, 97]
    # pixel_addr=[94, 92, 90, 88, 86, 84, 82, 80]
    # pixel_addr=[79, 77, 75, 73, 71, 69, 67, 65]
    # pixel_addr=[62, 60, 58, 56, 54, 52, 50, 48]
    # pixel_addr=[47, 45, 43, 41, 39, 37, 35, 33]
    # pixel_addr=[30, 28, 26, 24, 22, 20, 18, 16]
    # pixel_addr=[15, 13, 11, 9, 7, 5, 3, 1]
    # print(pixel_addr)