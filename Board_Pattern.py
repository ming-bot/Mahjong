import random
from copy import deepcopy
import numpy as np

class Pattern(object):
    def __init__(self, Number=0, Position=np.array([0, 0]), Parent=None):
        self.number = Number                  # 图案编号
        self.position = Position              # 位置信息
        self.turntimes = -1                   # 转弯次数
        self.cost = 0                         # 代价函数
        self.parent = Parent                  # 父节点
        self.direction = 0                    # 上一个点到这里的方向

    def path(self):
        """
        Returns list of Pattern from this pattern to the root pattern
        """
        pattern, path_back = self, []
        while pattern:
            path_back.append(pattern)
            pattern = pattern.parent
        return list(reversed(path_back))

    def __repr__(self):
        return "<Pattern {}(position={})(Cost={})>".format(self.number, self.position, self.cost)

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return self.position == other.position

class Map(object):
    def __init__(self, m, n, k, p,):
        self.row = m
        self.column = n
        self.pattern_class = p
        self.pattern_number = k
        self.map:list
        self.patternclasslist:list
        self.parent = None
        self.path = None
        self.cost = 0

    def mappath(self):
        """
        Returns list of map from this map to the root map
        """
        map, path_back = self, []
        while map:
            path_back.append(map)
            map = map.parent
        return list(reversed(path_back))
    
    def __repr__(self):
        return "<Map (Map={})(Path={})(Cost={})>".format(self.map, self.path, self.cost)

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return self.map == other.map
    

class Board(object):
    def __init__(self, m, n, p, k):
        self.row = m
        self.column = n
        self.pattern_class = p
        self.pattern_number = k
        self.map = []
        self.patternclasslist = []
        for i in range(p):
            self.patternclasslist.append([])
        for i in range(m + 2):
            self.map.append([])

    def Create_random_Board(self):
        list1 = []
        for i in range(self.pattern_number):      # 随机生成2k个图案
            r = random.randint(1, self.pattern_class)
            list1.append(r)
            list1.append(r)
        for i in range(self.row * self.column - 2 * self.pattern_number): # (mn-2k)地方都是0，表示没有图案
            list1.append(0)
        random.shuffle(list1)                     # 打乱
        for i in range((self.row + 2)*(self.column + 2)):
            if((i < (self.column + 2)) or (i % (self.column + 2) == 0) or \
                (i % (self.column + 2) == (self.column + 1)) or (i > (self.row + 1)*(self.column + 2))): # 边界点都是0图案，可以穿过。
                self.map[int(i/(self.column + 2))].append(0)
            else:
                r = list1.pop()
                self.map[int(i/(self.column + 2))].append(r)
                if r != 0:
                    self.patternclasslist[r - 1].append(Pattern(r, np.array([int(i/(self.column + 2)), i%(self.column + 2)]), None))  # 放进按照图案类型的map
        print("生成随机地图成功！")

    def Create_One_Board(self, boardlist):
        for i in range((self.row + 2)*(self.column + 2)):
            if((i < (self.column + 2)) or (i % (self.column + 2) == 0) or \
                (i % (self.column + 2) == (self.column + 1)) or (i > (self.row + 1)*(self.column + 2))): # 边界点都是-1图案，可以穿过，但是不能放置其他点
                self.map[int(i/(self.column + 2))].append(0)
            else:
                corx = int(i/(self.column + 2)) - 1
                cory = int(i%(self.column + 2)) - 1
                r = boardlist[corx][cory]
                self.map[corx + 1].append(r)
                if r != 0:
                    self.patternclasslist[r - 1].append(Pattern(r, np.array([int(i/(self.column + 2)), i%(self.column + 2)]), None))  # 放进按照图案类型的map
        print("指定地图生成成功！")

    def SetPattern(self, pattern, x, y):
        if(pattern < -1 or pattern > self.pattern_class):
            print("Error404：图案查找失败！")
            return
        if(x<= 0 or x >= self.row or y <= 0 or y >= self.column):
            print("Error303：超出边界！")
            return
        self.map[x][y] = pattern
        if pattern > 0:
            self.patternclasslist[pattern].append(Pattern(pattern, np.array([x, y]), None))
        print("设置图案成功！")

def Board_tran_Map(Board):
    aMap = Map(Board.row, Board.column, Board.pattern_class, Board.pattern_number)
    aMap.map = deepcopy(Board.map)
    aMap.patternclasslist = deepcopy(Board.patternclasslist)
    return aMap