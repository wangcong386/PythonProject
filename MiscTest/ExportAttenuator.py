from PySide6.QtCore import QPointF
import pandas as pd
import sqlite3

DB_TABLE_DISCALIBDATA = 'DBDistCalibData'
DB_TABLE_LIDAR_INFO = 'DBLidarInfo'

LSB4MM2M = 0.004
LSB2M = 0.000585362
M2ADCBITSLOPE = 26.6929
DICT_ERRORCODE = {0: '无数据', 1: '合格', 4: '数据中断', 8: '数据不足',
                  16: '斜率最大值过小', 32: '斜率最小值过大', 64: '第一段异常值过多', 128: '第二段异常值过多'}


def parserLidarInfo(lidarInfo):
    LidarSN = lidarInfo[0][0]
    LidarModel = lidarInfo[0][2]
    LaserCnt = lidarInfo[0][3]
    LoopGateList = eval(lidarInfo[0][4])['LoopGate']
    CalibDistList = eval(lidarInfo[0][5])['CalibDist']
    return [LidarSN, LidarModel, LaserCnt, LoopGateList, CalibDistList]


def parserCalibData(calibData):
    FCInfoList = []
    FCInfoDict = {}
    for data in calibData:
        info = FCInfo(data)
        # FCInfoList.append(info)
        # 字典FCInfoDict[通道][光强][距离]
        FCInfoDict[(info.LaserID, info.LoopGate,
                    info.CalibBoardCenterDist)] = info
    return FCInfoDict

# 寻找QPointFList中最大X对应的QPointF


def findMaxXQPointFList(list):
    if len(list) == 0:
        print('list is empty')
        return QPointF(0, 0)
    retPoint = list[0]
    for pair in list:
        if pair.x() > retPoint.x():
            retPoint.setX(pair.x())
            retPoint.setY(pair.y())
    return retPoint


def load_db_data(dbfile, csvoutput):
    con = sqlite3.connect(dbfile)
    cur = con.cursor()
    sqlGetDistCalibData = 'select * from ' + DB_TABLE_DISCALIBDATA
    sqlGetLidarInfo = 'select * from ' + DB_TABLE_LIDAR_INFO

    try:
        cur.execute(sqlGetDistCalibData)
        DistDataAll = cur.fetchall()
        cur.execute(sqlGetLidarInfo)
        LidarInfo = cur.fetchall()
        print(LidarInfo)
        LidarInfoList = parserLidarInfo(LidarInfo)
        LoopGateList = LidarInfoList[3]
        CalibDistList = LidarInfoList[4]
        CalibDataDict = parserCalibData(DistDataAll)
        DataSaveFrame = pd.DataFrame(columns=(
            'LaserID', 'LoopGate', 'CalibBoardDist', 'MaxSlopeAttenuator', 'MaxFrontAttenuator'))
        for laserID in range(128):
            for loopGate in LoopGateList:
                for CalibBoardDist in CalibDistList:
                    if (loopGate == LoopGateList[0] or loopGate == LoopGateList[2]) and CalibBoardDist == CalibDistList[3]:
                        print('laserID = {}, loopGate = {}, CalibBoardDist = {}'.format(
                            laserID, loopGate, CalibBoardDist))
                        DataPairListAttenuator = CalibDataDict[(
                            laserID, loopGate, CalibBoardDist)].RawDataAttenuator
                        pointAttenuatorMaxSlope = findMaxXQPointFList(
                            DataPairListAttenuator)
                        # 结果写入csv
                        DataSaveFrame = pd.concat([DataSaveFrame, pd.DataFrame({'LaserID': [laserID], 'LoopGate': [loopGate], 'CalibBoardDist': [
                            CalibBoardDist], 'MaxSlopeAttenuator': [pointAttenuatorMaxSlope.x()], 'MaxFrontAttenuator': [pointAttenuatorMaxSlope.y()]})], ignore_index=True)
        DataSaveFrame.to_csv(csvoutput, sep=',', index=False)
    except Exception as e:
        print(e)
        print('查询失败')
    finally:
        cur.close()
        con.close()


class FCInfo():
    def __init__(self, FCInfoRaw) -> None:
        self.Num = FCInfoRaw[0]
        self.Date = FCInfoRaw[1]
        self.LaserID = FCInfoRaw[2]
        self.LoopGate = FCInfoRaw[3]
        self.CalibBoardID = FCInfoRaw[4]
        self.RealDist = FCInfoRaw[5]
        self.CalibBoardCenterDist = FCInfoRaw[6]
        self.ArtificialOffset = FCInfoRaw[7]
        self.RawData = self.__parserRawData__(FCInfoRaw[8:136], 'RawData')
        self.RawDataAttenuator = self.__parserRawData__(
            FCInfoRaw[136:264], 'RawDataAttenuator')
        self.FittingPointPair = self.__parserFittingPoint__(
            FCInfoRaw[264], FCInfoRaw[265])
        self.Histogram = self.__parserHistogram__(FCInfoRaw[267])
        self.FittingFinished = FCInfoRaw[268]
        self.ErrorCode = DICT_ERRORCODE[FCInfoRaw[269]]

    def __parserRawData__(self, RawDataOrig, keyPattern):
        StatisticData = [eval(data) for data in RawDataOrig]
        RawDataPairList = []
        for dataSingleSlope in StatisticData:
            slopeList = list(dataSingleSlope.keys())
            # key只有一个'RawDataXXX'
            slopeVal = int(slopeList[0].split(keyPattern)[1])
            frontStatisticList = list(dataSingleSlope.values())
            # 展平列表
            frontStatisticList = [
                val for subList in frontStatisticList for val in subList]
            for statisSingleFront in frontStatisticList:
                RawDataPairList.extend([QPointF(
                    slopeVal, statisSingleFront[0]*LSB4MM2M - self.RealDist+self.ArtificialOffset)]*statisSingleFront[1])
        return RawDataPairList

    def __parserFittingPoint__(self, FCX, FCY):
        FittingPointX = eval(FCX)['FittingPointX']
        FittingPointY = eval(FCY)['FittingPointY']
        FittingPointPairList = [QPointF(round(FCXVal*M2ADCBITSLOPE), FCYVal*LSB2M+self.ArtificialOffset)
                                for FCXVal, FCYVal in zip(FittingPointX, FittingPointY)]
        return FittingPointPairList

    def __parserHistogram__(self, histo):
        Histogram = eval(histo)['Histogram']
        return Histogram


if __name__ == "__main__":
    # DB_PATH = '/home/hesai/Documents/DataAnalyse/AT/衰减片结果对比/AT3FCE5F9E3FC850/'
    DB_PATH = '/home/hesai/Documents/DataAnalyse/AT/衰减片结果对比/AT3FCE5F9E3FC850_2023_01_05_15_35_48/'
    dbfile = DB_PATH + 'DistCalibDB_2023-01-05-15-36-01.db'
    outputcsv = DB_PATH + 'Attenuator.csv'
    load_db_data(dbfile, outputcsv)
