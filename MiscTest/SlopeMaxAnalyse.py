# -*- coding: utf-8 -*-
'''
根据原始数据提取出的采样斜率最大值统计表，导出相应的最值/均值/方差并绘制图像保存，用于判定自适应阈值
'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import math
import os
import pandas as pd

DictBank = {
    'bank0/4': {
        0: [0, 2, 4, 6, 8, 10, 12, 14],
        4: [32, 34, 36, 38, 40, 42, 44, 46]
    },
    'bank8/12': {
        8: [64, 66, 68, 70, 72, 74, 76, 78],
        12: [96, 98, 100, 102, 104, 106, 108, 110]
    },
    'bank3/7': {
        3: [17, 19, 21, 23, 25, 27, 29, 31],
        7: [49, 51, 53, 55, 57, 59, 61, 63]
    },
    'bank11/15': {
        11: [81, 83, 85, 87, 89, 91, 93, 95],
        15: [113, 115, 117, 119, 121, 123, 125, 127]
    },
    'bank1/5': {
        1: [1, 3, 5, 7, 9, 11, 13, 15],
        5: [33, 35, 37, 39, 41, 43, 45, 47]
    },
    'bank9/13': {
        9: [65, 67, 69, 71, 73, 75, 77, 79],
        13: [97, 99, 101, 103, 105, 107, 109, 111]
    },
    'bank2/6': {
        2: [16, 18, 20, 22, 24, 26, 28, 30],
        6: [48, 50, 52, 54, 56, 58, 60, 62]
    },
    'bank10/14': {
        10: [80, 82, 84, 86, 88, 90, 92, 94],
        14: [112, 114, 116, 118, 120, 122, 124, 126]
    }
}
DictBankAveg = {
    'bank0/4': {
        0: 0,
        4: 0
    },
    'bank8/12': {
        8: 0,
        12: 0
    },
    'bank3/7': {
        3: 0,
        7: 0
    },
    'bank11/15': {
        11: 0,
        15: 0
    },
    'bank1/5': {
        1: 0,
        5: 0
    },
    'bank9/13': {
        9: 0,
        13: 0
    },
    'bank2/6': {
        2: 0,
        6: 0
    },
    'bank10/14': {
        10: 0,
        14: 0
    }
}
DictBankAvegDiff = {
    'bank0/4': 0,
    'bank8/12': 0,
    'bank3/7': 0,
    'bank11/15': 0,
    'bank1/5': 0,
    'bank9/13': 0,
    'bank2/6': 0,
    'bank10/14': 0
}


# 定义正态分布生成函数
def gd(plotX, ave=0, std=1):
    left = 1 / (np.sqrt(2 * math.pi) * np.sqrt(std))
    right = np.exp(-(plotX - ave)**2 / (2 * std))
    return left * right


# 导入数据
RESPATH = '/home/hesai/Documents/DataAnalyse/AT/20221212-0'
listFile = os.listdir(RESPATH)
for file in listFile:
    fileAbsPath = os.path.join(RESPATH, file)
    if (os.path.isfile(fileAbsPath) and fileAbsPath.endswith('.csv')):
        # 按照文件名先创建文件夹保存图片
        FolderName, FileSuffix = os.path.splitext(file)
        FolderAbsPath = os.path.join(RESPATH, FolderName)
        if (os.path.exists(FolderAbsPath) == False):
            os.mkdir(FolderAbsPath)
        # 读取当前csv文件
        AllLidarData = pd.read_csv(fileAbsPath)
        # 按行读取，从第二行开始
        # 获取行数
        AllLidarDataLineRange = AllLidarData.index
        for lineIdx in AllLidarDataLineRange:
            SingleLidarData = AllLidarData.iloc[[lineIdx]]
            # print(SingleLidarData)
            # 获取每行第一个值为雷达SN号
            SN = SingleLidarData.iloc[0, 0]
            # 接下来的128个数是每个通道SlopeMax
            SlopeMax = np.array(SingleLidarData.iloc[0, 1:129])
            MaxSlopeMax = np.max(SlopeMax)
            MinSlopeMax = np.min(SlopeMax)
            MeanSlopeMax = np.mean(SlopeMax)
            MeanSlopeMaxArr = np.ones((128, 1)) * MeanSlopeMax
            MeanSlopeMaxArr80 = MeanSlopeMaxArr * 0.8
            SlopeIdx = np.arange(128)

            # 接下来从129到257是FrontOfSlopeMax
            FrontOfSlopeMax = np.array(SingleLidarData.iloc[0, 129:257]) - 2
            # 接下来258=Mean，259=Max，260=Min，261=Std
            # 接下来从261开始，每5个数为一组FrontTrend
            # FrontTrend = np.array(
            #     SingleLidarData.iloc[0, 261:901]).reshape((128, 5))
            # print(FrontTrend)

            # **********绘制图像并保存：128通道斜率最大值
            # 画布大小
            plt.figure(figsize=(30, 4))
            # 散点图
            plt.scatter(SlopeIdx, SlopeMax, c='red', label='SlopeMax')
            # 均值
            plt.plot(SlopeIdx, MeanSlopeMaxArr, c='green', label='Mean')
            # 均值*0.8
            plt.plot(SlopeIdx, MeanSlopeMaxArr80, c='blue', label='Mean*0.8')
            # y轴取值范围
            plt.ylim([MinSlopeMax - 10, MaxSlopeMax + 10])
            # x轴坐标刻度
            plt.xticks(SlopeIdx, rotation=45)
            plt.xlabel("LaserID")
            plt.ylabel("SlopeMax")
            plt.legend()
            ImgSavePath = os.path.join(FolderAbsPath, SN)
            print(ImgSavePath)
            plt.savefig(ImgSavePath, bbox_inches='tight')
            plt.close()

            # **********绘制图像并保存：128通道拟合截止点前沿最大值
            MeanFrontOfSlopeMax = np.mean(FrontOfSlopeMax)
            MaxFrontOfSlopeMax = np.max(FrontOfSlopeMax)
            MinFrontOfSlopeMax = np.min(FrontOfSlopeMax)
            MeanFrontOfSlopeMaxArr = np.ones((128, 1)) * MeanFrontOfSlopeMax
            MeanFrontOfSlopeMax80 = MeanFrontOfSlopeMaxArr * 0.8
            MeanFrontOfSlopeMax120 = MeanFrontOfSlopeMaxArr * 1.2
            # 画布大小
            plt.figure(figsize=(30, 4))
            # 散点图
            plt.scatter(SlopeIdx,
                        FrontOfSlopeMax,
                        c='red',
                        label='FrontOfSlopeMax')
            # 均值
            plt.plot(SlopeIdx, MeanFrontOfSlopeMaxArr, c='green', label='Mean')
            # 均值*0.8
            plt.plot(SlopeIdx,
                     MeanFrontOfSlopeMax80,
                     c='blue',
                     label='Mean*0.8')
            # 均值*1.2
            plt.plot(SlopeIdx,
                     MeanFrontOfSlopeMax120,
                     c='blue',
                     label='Mean*1.2')
            # y轴取值范围
            plt.ylim([MinFrontOfSlopeMax - 0.1, MaxFrontOfSlopeMax + 0.1])
            # x轴坐标刻度
            plt.xticks(SlopeIdx, rotation=45)
            plt.xlabel("LaserID")
            plt.ylabel("FrontOfSlopeMax")
            plt.legend()
            ImgSavePath = os.path.join(FolderAbsPath, 'FrontOfSlopeMax_' + SN)
            print(ImgSavePath)
            plt.savefig(ImgSavePath, bbox_inches='tight')
            plt.close()
'''
            # 统计同bank上下两部分均值差异
            # 获取同bank通道组号
            for bankName in DictBank.keys():
                DictSingleBank = DictBank[bankName]
                keyIdx = 0
                for laserGroup in DictSingleBank.keys():
                    halfBankIdx = DictSingleBank[laserGroup]
                    SlopeMaxHalfBank = SlopeMax[halfBankIdx]
                    DictBankAveg[bankName][laserGroup] = np.mean(
                        SlopeMaxHalfBank)
                    if (keyIdx == 0):
                        DictBankAvegDiff[bankName] = DictBankAveg[bankName][laserGroup]
                    elif (keyIdx == 1):
                        DictBankAvegDiff[bankName] -= DictBankAveg[bankName][laserGroup]
                        DictBankAvegDiff[bankName] = abs(
                            DictBankAvegDiff[bankName])
                    keyIdx += 1

            # **********绘制图像并保存:8个bank上下差异

            # 画布大小
            plt.figure(figsize=(12, 4))
            # 散点图
            BankList = DictBankAvegDiff.keys()
            BankDiffValues = DictBankAvegDiff.values()
            plt.scatter(
                BankList, BankDiffValues, c='red', label='SlopeMaxBankAvegDiff')
            # y轴取值范围
            plt.ylim([0, 20])
            plt.xlabel("BankName")
            plt.ylabel("SlopeMaxBankAvegDiff")
            plt.legend()
            ImgSavePath = os.path.join(
                FolderAbsPath, 'SlopeMaxBankAvegDiff_'+SN)
            print(ImgSavePath)
            plt.savefig(ImgSavePath, bbox_inches='tight')
            plt.close()

            # **********绘制图像并保存:128通道截止前n个点变化趋势

            # 画布大小
            plt.figure(figsize=(30, 4))
            # 颜色列表
            ColorList = ['red', 'orange', 'yellow', 'green', 'cyan']
            # 散点图
            for DrawIdx in range(5):
                plt.scatter(
                    SlopeIdx, FrontTrend[:, DrawIdx], c=ColorList[DrawIdx], label='FrontTrend{}'.format(DrawIdx))
            # y轴取值范围
            plt.ylim([0, 20])
            # x轴坐标刻度
            plt.xticks(SlopeIdx, rotation=45)
            plt.xlabel("LaserID")
            plt.ylabel("FrontTrend")
            plt.legend()
            ImgSavePath = os.path.join(
                FolderAbsPath, 'FrontTrend_'+SN)
            print(ImgSavePath)
            plt.savefig(ImgSavePath, bbox_inches='tight')
            plt.close()
'''
