from basic_search import *
from Board_Pattern import *
import sortedcontainers
import numpy as np

# 将map转换为整型数进行存储
def map_tran(Map):
    result = 0
    for i in range(1, Map.row):
        for j in range(1, Map.column):
            result += Map.map[i][j] * ((Map.pattern_class + 1) ** ((Map.column) * (i - 1) + j - 1))
    return result

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
                        mymap = Board_tran_Map(Map)
                        Remove(mymap, mymap.patternclasslist[index], i, j)
                        mymap.parent = Map
                        mymap.cost = Map.cost + path[-1].turntimes
                        mymap.path = deepcopy(list(path))
                        next_move.append(mymap)
    return next_move


def Leastcost_link(Board):
    init = Board_tran_Map(Board)           # 最初的Map
    # list0 = Zeroturn_link(Board)         # 第一次零刷
    # if list0 != False:                   # 零刷更新
    #     firststep = Board_tran_Map(Board)
    #     firststep.parent = init
    #     firststep.path = list0
    #     firststep.cost = Board.pattern_number - len(list0)  #cost是棋盘上面存在的现有点
    #     Unsearch = PriorityQueue(firststep)
    # else:
    Unsearch = PriorityQueue(init)
    Searched = set()
    '''
    将Unsearch队列中的map取出至Searched，将可能的下一个Node再排入Unsearch
    '''
    while Unsearch.empty() == 0:
        # 取出第一个
        Current_Search = Unsearch.pop()
        if np.sum(np.array(Current_Search.map)) == 0: # 对所有元素进行求和
            break
        # 放入已搜索中
        Searched.add(map_tran(Current_Search))
        # 可能的改变点
        NextMapList = next_map(Current_Search)
        for next_map1 in NextMapList:
            Unsearch.push(next_map1)
            # vaild_next = Board_tran_Map(next_map1)
            # vaild_next.parent = next_map1.parent
            # vaild_next.path = next_map1.path
            # vaild_next.cost = next_map1.cost         # 对象的深拷贝
            # list1 = Zeroturn_link(vaild_next)
            # if list1 != False:
            #     for listitem in list1:
            #         vaild_next.path.append(listitem)
            # Unsearch.push(vaild_next)
            # print(vaild_next)
            # print("--------------------------------------\n")
    print(Current_Search.mappath())
    return Current_Search.mappath()

