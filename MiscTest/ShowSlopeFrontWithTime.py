# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtChart import QChartView, QChart, QScatterSeries, QValueAxis
import os
import sys
import numpy as np
import pandas as pd

DataFile = '/home/hesai/Documents/工程/AT128距离校准/新分板策略数据分析/SampleDataRaw/ExportRawData_LaserID20_LoopGate24.csv'
# csv导入slope/front/time数据
df = pd.read_csv(DataFile, header=None, sep=',')
df_np = df.to_numpy()
col_time = df_np[:, 0]
col_slope = df_np[:, 1]
col_front = df_np[:, 2]
col_stamp = df_np[:, 3]
# print(col_time)
# print(col_slope)
# print(col_front)

# 加入时间轴，控制时间，绘制(slope,front)点
# 将所有数据分为n段，分段显示
DataSeg = 100
SegCnt = np.size(col_time) // DataSeg
# for segIdx in range(DataSeg):
#     seg_slope = col_slope[(segIdx * SegCnt):((segIdx + 1) * SegCnt)]
#     seg_front = col_front[(segIdx * SegCnt):((segIdx + 1) * SegCnt)]


class ShowGraph(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.initUI()

    def initUI(self):
        # 垂直布局
        self.layout = QVBoxLayout()
        size = QSizePolicy(QSizePolicy.Policy.Preferred,
                           QSizePolicy.Policy.Preferred)
        size.setVerticalStretch(1)

        # 添加滑块
        self.sld_time = QSlider(Qt.Orientation.Horizontal, self)
        # 滑块位置/大小
        self.sld_time.setGeometry(500, 800, 500, 30)
        self.sld_time.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.sld_time.setMinimum(0)
        self.sld_time.setMaximum(np.size(col_time) - 1)
        self.sld_time.setSingleStep(3)

        self.sld_time.valueChanged[int].connect(self.changeTime)
        self.sld_time.setSizePolicy(size)
        self.layout.addWidget(self.sld_time)

        # 添加图表
        size.setVerticalStretch(5)

        self.slope_front_series = QScatterSeries(self)

        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.AllAnimations)
        self.addSeries('slope-front')

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setSizePolicy(size)
        self.chart_view.setRubberBand(
            QChartView.RubberBand.RectangleRubberBand)
        self.layout.addWidget(self.chart_view)

        self.setLayout(self.layout)

    def changeTime(self, value):
        print('当前时刻', value, col_time[value], '当前点时间戳', col_stamp[value])
        print('当前点数', self.series.count())
        # print('期望删除点数', self.series.count() - value)
        # self.series.removePoints(value, self.series.count() - value)
        new_point = QPointF()
        new_point.setX(col_slope[value])
        new_point.setY(col_front[value])
        # self.series.replace(0, new_point)
        self.series.append(new_point)

    def addSeries(self, name):
        self.series = QScatterSeries()
        self.series.setMarkerShape(
            QScatterSeries.MarkerShape.MarkerShapeCircle)
        self.series.setMarkerSize(15.0)
        self.series.setName(name)

        # 使用初值初始化

        self.series.append(df_np[0, 1], df_np[0, 2])

        self.chart.addSeries(self.series)

        # set X-Axis
        self.axis_slope = QValueAxis()
        self.axis_slope.setTitleText('Slope')
        self.axis_slope.setMin(min(col_slope) - 10)
        self.axis_slope.setMax(max(col_slope) + 10)
        self.chart.addAxis(self.axis_slope, Qt.AlignmentFlag.AlignBottom)
        self.series.attachAxis(self.axis_slope)

        # set Y-Axis
        self.axis_front = QValueAxis()
        self.axis_front.setTitleText('Front')
        self.axis_front.setMin(min(col_front) - 10)
        self.axis_front.setMax(max(col_front) + 10)
        self.chart.addAxis(self.axis_front, Qt.AlignmentFlag.AlignLeft)
        self.series.attachAxis(self.axis_front)


class Window(QMainWindow):
    def __init__(self, widget):
        print("Qt5 Version Number is: {0}".format(QT_VERSION_STR))
        print("PyQt5 Version is: {}".format(PYQT_VERSION_STR))
        # print("Sip Version is: {}".format(SIP_VERSION_STR))
        QMainWindow.__init__(self)
        self.setWindowTitle('Slope-Front-TimeShow')
        self.setCentralWidget(widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    graph = ShowGraph()
    win = Window(graph)
    win.showMaximized()
    sys.exit(app.exec_())
