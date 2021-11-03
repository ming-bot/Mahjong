from totalSearch import *
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


