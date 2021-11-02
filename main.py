from Board_Pattern import *
from basic_search import *
from totalSearch import *
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal


# 求解问题的线程
class SolveThread(QThread):
    Solved = pyqtSignal(list)
    Path = []

    def __init__(self, game=None, rule_flag=0):
        super(SolveThread, self).__init__()
        self.Game = game
        self.RuleFlag = rule_flag

    def run(self) -> None:
        if self.RuleFlag == 0:
            self.Path = limit_link(self.Game, 2)
            self.Solved.emit(self.Path)
        elif self.RuleFlag == 1:
            self.Path = Leastcost_link(self.Game)
            self.Solved.emit(self.Path)


if __name__ == "__main__":
    # m = input("请输入地图的长：")
    # n = input("请输入地图的宽：")
    # p = input("请输入图案的种类：")
    # k = input("请输入图案的数目：")  # 这里还要处理输入数据是否合法
    board = Board(5, 5, 5, 12)
    mymap = np.array([[4, 4, 5, 5, 2], [2, 3, 3, 4, 5], [2, 0, 4, 2, 2], [4, 2, 1, 1, 2], [4, 5, 2, 2, 2]])
    board.Create_One_Board(mymap)
    # board.Create_random_Board()
    print(board.map)
    print(board.patternclasslist)
    # p1 = Pattern(3, np.array([1,2]), None)
    # p2 = Pattern(3, np.array([3,2]), None)
    # Dot_to_Dot(board, p1, p2, 2)

    # print(Zeroturn_link(board))
    # print(board.map)
    # print(board.patternclasslist)

    Leastcost_link(board)
