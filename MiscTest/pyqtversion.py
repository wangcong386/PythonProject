from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = QWidget()
    w.resize(640, 320)
    w.move(400, 200)
    w.setWindowTitle("Empty Window")
    w.show()
    print("Qt5 Version Number is: {0}".format(QT_VERSION_STR))
    print("PyQt5 Version is: {}".format(PYQT_VERSION_STR))

    sys.exit(app.exec_())