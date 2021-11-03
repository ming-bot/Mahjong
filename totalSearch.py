from basic_search import *
from Board_Pattern import *
import sortedcontainers
import numpy as np

# 将map转换为整型数进行存储
def map_tran(Map):
    result = 0
    for i in range(1, Map.row + 1):
        for j in range(1, Map.column + 1):
            if Map.map[i][j] != 0:
                result += 2 ** ((Map.column) * (i - 1) + j - 1)
    return result

# 预期的cost，本质上是如果行列都没有，代价至少为1
def est_cost(patternlist):
    he = 0
    for item1 in patternlist:
        Yes = 1
        for item2 in patternlist:
            if all(item1 == item2):
                continue
            if(item1.position[0] == item2.position[0] or item1.position[1] == item2.position[1]):
                Yes = 0
        if Yes == 1:
            he += 0.5
    return he


# 返回的是一个充满Map的列表
def next_map(Map):
    next_move = []
    limit = -1
    while len(next_move) == 0:
        limit += 1
        mapclass_num = Map.patternclasslist
        for index, class_num in enumerate(mapclass_num):
            for i in range(len(class_num) - 1):
                for j in range(i + 1, len(class_num)):
                    path = Dot_to_Dot(Map, class_num[i], class_num[j], limit)
                    if path != False:
                        mymap = Map_to_Map(Map)
                        Remove(mymap, mymap.patternclasslist[index], i, j)
                        mymap.beibeicost[index] = est_cost(mymap.patternclasslist[index])
                        mymap.parent = Map
                        mymap.i_cost = Map.i_cost + path[-1].turntimes * (mymap.pattern_number + 1) - 1
                        mymap.cost = mymap.i_cost + sum(mymap.beibeicost) * (mymap.pattern_number + 1)
                        mymap.path.append(deepcopy(list(path)))
                        next_move.append(mymap)
    return next_move


def Leastcost_link(Board):
    num = np.argwhere(np.array(Board.map == -1)).shape[0]
    init = Map(Board.row, Board.column, Board.pattern_class, Board.pattern_number)           # 最初的Map
    init.map = deepcopy(Board.map)
    init.patternclasslist = deepcopy(Board.patternclasslist)
    for index, item in enumerate(init.patternclasslist):
        init.beibeicost[index] = est_cost(item)
    init.i_cost = init.pattern_number      # 最初的代价
    Unsearch = PriorityQueue(init)
    Searched = set()
    '''
    将Unsearch队列中的map取出至Searched，将可能的下一个Node再排入Unsearch
    '''
    while Unsearch.empty() == 0:
        # 取出第一个
        Current_Search = Unsearch.pop()
        if np.sum(np.array(Current_Search.map)) == -num:  # 对所有元素进行求和
            break
        # 放入已搜索中
        Searched.add(map_tran(Current_Search))
        # 可能的改变点
        NextMapList = next_map(Current_Search)
        for next_map1 in NextMapList:
            Unsearch.push(next_map1)
    return Current_Search.mappath()

def FakeLeastcost_link(Board):
    num = np.argwhere(np.array(Board.map == -1)).shape[0]
    init = Map(Board.row, Board.column, Board.pattern_class, Board.pattern_number)  # 最初的Map
    init.map = deepcopy(Board.map)
    init.patternclasslist = deepcopy(Board.patternclasslist)
    for index, item in enumerate(init.patternclasslist):
        init.beibeicost[index] = est_cost(item)
    init.i_cost = init.pattern_number      # 最初的代价
    list0 = Zeroturn_link(Board)           # 第一次零刷
    if list0 != False:                     # 零刷更新
        firststep = Map(Board.row, Board.column, Board.pattern_class, Board.pattern_number)  # 最初的Map
        firststep.map = deepcopy(Board.map)
        firststep.patternclasslist = deepcopy(Board.patternclasslist)
        for index, item in enumerate(firststep.patternclasslist):
            firststep.beibeicost[index] = est_cost(item)
        firststep.i_cost = init.pattern_number - len(list0)  # 最初的代价
        firststep.parent = init
        firststep.path = list0
        Unsearch = PriorityQueue(firststep)
    else:
        Unsearch = PriorityQueue(init)
    Searched = set()
    '''
    将Unsearch队列中的map取出至Searched，将可能的下一个Node再排入Unsearch
    '''
    while Unsearch.empty() == 0:
        # 取出第一个
        Current_Search = Unsearch.pop()
        if np.sum(np.array(Current_Search.map)) == -num:  # 对所有元素进行求和
            break
        # 放入已搜索中
        Searched.add(map_tran(Current_Search))
        # 可能的改变点
        NextMapList = next_map(Current_Search)
        for next_map1 in NextMapList:
            vaild_next = Map_to_Map(next_map1)
            vaild_next.parent = next_map1.parent
            vaild_next.path = deepcopy(next_map1.path)
            vaild_next.beibeicost = deepcopy(next_map1.beibeicost)
            list1 = Zeroturn_link(vaild_next)
            vaild_next.i_cost = next_map1.i_cost
            vaild_next.cost = next_map1.cost
            if list1 != False:
                vaild_next.i_cost = vaild_next.i_cost - len(list1)
                vaild_next.cost = vaild_next.cost - len(list1)
                for listitem in list1:
                    vaild_next.path.append(listitem)
            Unsearch.push(vaild_next)
    return Current_Search.mappath()
