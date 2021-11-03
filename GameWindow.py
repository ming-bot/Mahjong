from MahjongUI import *
import time
from PyQt5.Qt import *
from main import *
import numpy as np
import sys


# 消除动画的线程
class EliminateThread(QThread):
    EliminateFinished = pyqtSignal()
    CostSignal = pyqtSignal(str)

    def __init__(self, tbw_game=None, unit_path=None):
        super(EliminateThread, self).__init__()
        self.tbw_game = tbw_game
        self.UnitAndPath = unit_path
        self.cost = 0

    def Eliminate(self, unit_path):
        for map1 in unit_path:
            for link_line in map1.path:
                for pt in link_line:
                    x = pt.position[0]
                    y = pt.position[1]
                    self.tbw_game.item(x, y).setBackground(QColor(132, 133, 135))
                    self.tbw_game.viewport().update()
                    time.sleep(0.05)
                time.sleep(0.3)
                # 消除
                x1 = link_line[0].position[0]
                y1 = link_line[0].position[1]
                x2 = link_line[-1].position[0]
                y2 = link_line[-1].position[1]

                self.tbw_game.item(x1, y1).setIcon(QIcon("./JEPG/0.jpg"))
                self.tbw_game.item(x2, y2).setIcon(QIcon("./JEPG/0.jpg"))
                self.tbw_game.viewport().update()

                # 恢复颜色
                for pt in link_line:
                    x = pt.position[0]
                    y = pt.position[1]
                    self.tbw_game.item(x, y).setBackground(QColor(255, 255, 255, 0))
                    self.tbw_game.viewport().update()

                self.cost = self.cost + link_line[-1].turntimes
                self.CostSignal.emit(str(self.cost))

    def run(self) -> None:
        self.Eliminate(self.UnitAndPath)
        time.sleep(0.5)

        self.EliminateFinished.emit()


class GameWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(GameWindow, self).__init__()
        self.setupUi(self)
        self.SThread = SolveThread()
        self.EThread = EliminateThread()
        self.setWindowIcon(QIcon('./JEPG/id.jpg'))
        self.cost = 0

        pll = self.tableWidget.palette()
        pll.setBrush(QPalette.Base, QBrush(QColor(255, 255, 255, 100)))
        self.tableWidget.setPalette(pll)

        self.tableWidget.horizontalHeader().setHidden(True)
        self.tableWidget.verticalHeader().setHidden(True)  # 隐藏表头
        self.tableWidget.setShowGrid(False)  # 隐藏线
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 不可更改

        self.board = Board(0,0,0,0)
        self.mode = 0
        self.autoSolve.setEnabled(False)

        timer = QTimer(self)
        timer.timeout.connect(self.showtime)
        timer.start()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def paintEvent(self, event):  # set background_img
        painter = QPainter(self)
        painter.drawRect(self.rect())
        pixmap = QPixmap('./JEPG/background.jpg')  # 换成自己的图片的相对路径
        painter.drawPixmap(self.rect(), pixmap)

    def slot_oneboard_clicked(self):
        self.autoSolve.setEnabled(True)
        m = int(self.lineEdit.text())
        n = int(self.lineEdit_2.text())
        p = int(self.lineEdit_3.text())
        k = int(self.lineEdit_4.text())
        if m < 0 or n < 0 or p > (m * n) or k > (m * n) / 2:
            msg_box = QMessageBox.warning(self, 'Error', '数据不合法!', QMessageBox.Cancel)
            if msg_box == QMessageBox.Cancel:
                return
        self.board = Board(m, n, p, k)
        onemap = eval(self.textEdit.toPlainText())
        self.board.Create_One_Board(np.array(onemap))
        # 清空
        self.tableWidget.clear()
        # 设置行列数
        self.tableWidget.setRowCount(m + 2)
        self.tableWidget.setColumnCount(n + 2)
        # 设置总大小和各个格子大小
        self.tableWidget.setFixedSize((n + 2) * 50 + 2, (m + 2) * 50 + 2)
        for i in range(m + 2):
            self.tableWidget.setRowHeight(i, 50)
        for j in range(n + 2):
            self.tableWidget.setColumnWidth(j, 50)
        self.tableWidget.setIconSize(QSize(45, 45))
        # 放置图片
        for i in range(m + 2):
            for j in range(n + 2):
                item = QTableWidgetItem()
                kind = self.board.map[i][j]
                if kind > -2:
                    item.setIcon(QIcon(QPixmap("./JEPG/" + str(kind) + ".jpg")))
                    self.tableWidget.setItem(i, j, item)
                else:
                    self.tableWidget.setItem(i, j, item)

    def slot_begin_button_clicked(self):
        self.autoSolve.setEnabled(True)
        m = int(self.lineEdit.text())
        n = int(self.lineEdit_2.text())
        p = int(self.lineEdit_3.text())
        k = int(self.lineEdit_4.text())
        if m < 0 or n < 0 or p > (m * n) or k > (m * n) / 2:
            msg_box = QMessageBox.warning(self, 'Error', '数据不合法!', QMessageBox.Cancel)
            if msg_box == QMessageBox.Cancel:
                return
        self.board = Board(m, n, p, k)
        self.board.Create_random_Board()
        # 清空
        self.tableWidget.clear()
        # 设置行列数
        self.tableWidget.setRowCount(m + 2)
        self.tableWidget.setColumnCount(n + 2)
        # 设置总大小和各个格子大小
        self.tableWidget.setFixedSize((n + 2) * 70 + 2, (m + 2) * 70 + 2)
        for i in range(m + 2):
            self.tableWidget.setRowHeight(i, 70)
        for j in range(n + 2):
            self.tableWidget.setColumnWidth(j, 70)
        self.tableWidget.setIconSize(QSize(65, 65))
        # 放置图片
        for i in range(m + 2):
            for j in range(n + 2):
                item = QTableWidgetItem()
                kind = self.board.map[i][j]
                if kind > 0:
                    item.setIcon(QIcon(QPixmap("./JEPG/" + str(kind) + ".jpg")))
                    self.tableWidget.setItem(i, j, item)
                else:
                    self.tableWidget.setItem(i, j, item)

    def slot_autoSolve_clicked(self):
        self.autoSolve.setEnabled(False)
        self.begin_button.setEnabled(False)
        self.oneboard.setEnabled(False)
        self.label_5.setText("当前代价：0")
        self.imag_show_function()
        self.SThread = SolveThread(self.board, self.mode)
        self.SThread.start()
        self.SThread.Solved.connect(self.GameSolved)

    def GameSolved(self, Path):
        # 启动消除的动画线程
        self.EThread = EliminateThread(self.tableWidget, Path)
        self.EThread.start()
        self.EThread.CostSignal.connect(self.UpdateCost)
        self.EThread.EliminateFinished.connect(self.EliminateFinished)

    def EliminateFinished(self):
        self.begin_button.setEnabled(True)
        self.oneboard.setEnabled(True)

    def slot_GameMode_currentIndexChanged(self):
        self.mode = self.GameMode.currentIndex()
        pass

    def UpdateCost(self, cost):
        self.label_5.setText("当前代价：" + cost)

    def showtime(self):
        datetime = QDateTime.currentDateTime()
        text = datetime.toString()
        self.label_6.setText(text)

    def imag_show_function(self):
        dialog_fault = QDialog()
        image_path = "./JEPG/pay.jpg"
        pic = QPixmap(image_path)
        dialog_fault.setWindowTitle("哈哈哈:)")
        label_pic = QLabel("show", dialog_fault)
        label_pic.setPixmap(pic)
        label_pic.setGeometry(20, 10, 200, 300)
        dialog_fault.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GameWindow()
    ex.paintEngine()
    ex.show()
    sys.exit(app.exec_())
