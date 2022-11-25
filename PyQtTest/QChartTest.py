import os, sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QSizePolicy
from PyQt5.QtChart import QChart, QChartView
from PyQt5.QtGui import QPainter


class TestWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.AllAnimations)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        self.main_layout = QHBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size.setHorizontalStretch(1)

        size.setHorizontalStretch(4)
        self.chart_view.setSizePolicy(size)
        self.main_layout.addWidget(self.chart_view)

        self.setLayout(self.main_layout)


class MainWindow(QMainWindow):

    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Test Win")
        self.setCentralWidget(widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = TestWidget()
    win = MainWindow(widget)
    win.show()
    sys.exit(app.exec())