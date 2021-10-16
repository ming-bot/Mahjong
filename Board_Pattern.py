import random
import numpy as np

class Pattern(object):
    def __init__(self, Number=0, Position=np.array([0, 0]), Cost=0xffff, Parent=None, Direction=None):
        self.number = Number                  # 图案编号
        self.position = Position              # 位置信息
        self.cost = Cost                      # 代价函数
        self.parent = Parent                  # 父节点
        self.direction = Direction            # 上一个点到这里的方向
        self.turn = 0                         # 记录转弯次数
    
    def __repr__(self):
        return "<Pattern {}(position={})(Cost={})>".format(self.number, self.position, self.cost)

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return self.number == other.number

class Board(Pattern):
    def __init__(self, m, n, k, p):
        self.row = m
        self.column = n
        self.pattern_class = p
        self.pattern_number = k
        self.maplist = []
        self.patternclasslist = []
        for i in range(p + 1):
            self.patternclasslist.append([])

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
                (i % (self.column + 2) == (self.column + 1)) or (i > (self.row + 1)*(self.column + 2))): # 边界点都是-1图案，可以穿过，但是不能放置其他点
                self.maplist.insert(i, -1)
            else:
                r = list1.pop()
                self.maplist.insert(i, r)
                self.patternclasslist[r].append(Pattern(r, np.array([int(i/(self.column + 2)), i%(self.column + 2)]), 0xffff, None, None))  # 放进按照图案类型的map
        print("生成随机地图成功！")

    def Create_One_Board(self, boardlist):
        for i  in range((self.row + 2)*(self.column + 2)):
            if((i < (self.column + 2)) or (i % (self.column + 2) == 0) or \
                (i % (self.column + 2) == (self.column + 1)) or (i > (self.row + 1)*(self.column + 2))): # 边界点都是-1图案，可以穿过，但是不能放置其他点
                self.maplist.insert(i, -1)
            else:
                corx = int(i/(self.column + 2)) - 1
                cory = int(i%(self.column + 2)) - 1
                r = boardlist[corx][cory]
                self.maplist.insert(i, r)
                self.patternclasslist[r].append(Pattern(r, np.array([int(i/(self.column + 2)), i%(self.column + 2)]), 0xffff, None, None))  # 放进按照图案类型的map
        print("指定地图生成成功！")

    def SetPattern(self, pattern, x, y):
        if(pattern < 0 or pattern > self.pattern_class):
            print("Error404：图案查找失败！")
            return
        if((x + 1) <= 0 or (x + 1) >= (self.row + 1) or (y + 1) <= 0 or (y + 1) >= (self.column + 1)):
            print("Error303：超出边界！")
            return
        list_position = (x + 1) * (self.column + 2) + (y + 1)
        self.maplist[list_position] = pattern
        self.patternclasslist[pattern].append(Pattern(pattern, np.array([x + 1, y + 1]), 0xffff, None, None))
        print("设置图案成功！")

