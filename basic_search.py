from Board_Pattern import *
import sortedcontainers
import numpy as np

class PriorityQueue(object):

    def __init__(self, node):
        self._queue = sortedcontainers.SortedList([node])

    def push(self, node):
        self._queue.add(node)

    def pop(self):
        return self._queue.pop(index=0)

    def empty(self):
        return len(self._queue) == 0

    def compare_and_replace(self, i, node):
        if node < self._queue[i]:
            self._queue.pop(index=i)
            self._queue.add(node)

    def find(self, node):
        for i in range(len(self._queue)):
            if(all(self._queue[i] == node)):
                return True
        return False

def IsNotBlocked(Board, corx, cory):
    if(Board.map[corx][cory] == 0):
        return True
    else:
        return False

def Isvalid(Board, loc):
    if -1 < loc[0] < Board.row + 2 and -1 < loc[1] < Board.column + 2:
        return True
    else:
        return False

def next_move(Board, corx, cory, goalcor):
    if(abs(corx - goalcor[0]) + abs(cory - goalcor[1]) == 1):
        return [goalcor]
    candidates = [[corx-1, cory], [corx+1, cory],[corx, cory-1], [corx, cory+1]]
    valid_candidates = []
    for item in candidates:
        if((Isvalid(Board, item)) and (IsNotBlocked(Board, item[0], item[1])) == True):
            valid_candidates.append(np.array(item))
    return valid_candidates

# 将坐标转换为int型存储
def cor_tran(Board, cor):
    result = (Board.column + 2) * cor[0] + cor[1]
    return result

def manhadun_cost(current_cor, goal_cor):
    manhadun = abs(current_cor[0] - goal_cor[0]) + abs(current_cor[1] - goal_cor[1])
    return manhadun

def Create_turntimes(Board, pattern, cor):
    Direction = cor[0] - pattern.position[0] + 2 * (cor[1] - pattern.position[1]) # 1表示向下，-1向上，2向右，-2向左
    pa = Board.map[cor[0]][cor[1]]
    p = Pattern(pa, cor, pattern)
    p.direction = Direction
    if Direction != pattern.direction:
        p.turntimes = pattern.turntimes + 1
    else:
        p.turntimes = pattern.turntimes
    return p

def Remove(Board, line, i, j): # 注意i < j
    begin = line[i]
    end = line[j]
    line.pop(i)
    line.pop(j - 1)
    Board.map[begin.position[0]][begin.position[1]] = 0
    Board.map[end.position[0]][end.position[1]] = 0

# Dot_to_Dot函数负责测定两点之间在不超过limit次转弯的基础上能不能消除，若能返回路径，不能就返回False
#
def Dot_to_Dot(Board, begin, end, limit):
    # 初始化队列
    begin.cost = manhadun_cost(begin.position, end.position)
    Unsearch = PriorityQueue(begin)
    Searched = set()
    IsSearch = False
    '''
    将Unsearch队列中的pattern取出至Searched，将可能的下一个Node再排入Unsearch
    '''
    while Unsearch.empty() == 0:
        if IsSearch == True:
            break
        # 取出第一个
        Current_Search = Unsearch.pop()
        # 放入已搜索中
        Searched.add(cor_tran(Board, Current_Search.position))
        # 可能的改变点
        valid_candidates = next_move(Board, Current_Search.position[0], Current_Search.position[1], end.position)
        for vaild_candidate in valid_candidates:
            Next_Node = Create_turntimes(Board, Current_Search, vaild_candidate)
            if(Next_Node.turntimes > limit):
                continue
            if all(Next_Node == end):
                Next_Node.cost = (Board.row + 2) * (Board.column + 2) * Next_Node.turntimes
                # print(Next_Node.cost)
                # print("预消除两个点为：")
                # print(begin,"-------------->", end)
                IsSearch = True
                break

            if((Unsearch.find(Next_Node) or Searched.__contains__(cor_tran(Board, Next_Node.position))) == False):
                Next_Node.cost = (Board.row + 2) * (Board.column + 2) * Next_Node.turntimes + manhadun_cost(Next_Node.position, end.position)
                # print(Next_Node.cost)
                # print(Next_Node)
                Unsearch.push(Next_Node)
    if IsSearch:
        # print("搜索的路径为：\n")
        # print(Next_Node.path())
        return (Next_Node.path())
    else:
        # print('None!Not found a path!')
        return False

# Zeroturn_link“零刷”函数负责找到不需要转弯就能消的点，并且返回一共消的几条路径
# 并且他会不断刷，直到不存在满足转弯次数==0就能消的点，返回False
def Zeroturn_link(Board):
    link_num = -1
    link_list = []
    while link_num != 0:
        link_num = 0
        patternclass_num = Board.patternclasslist
        for class_num in patternclass_num:
            for i in range(len(class_num) - 1):
                if(i >= len(class_num) - 1):
                    break
                for j in range(i + 1, len(class_num)):
                    if(j >= len(class_num)): # pop出去了一些节点
                        break
                    path = Dot_to_Dot(Board, class_num[i], class_num[j], 0)
                    if path != False:
                        link_list.append(path)
                        link_num += 1
                        Remove(Board, class_num, i, j)
    if len(link_list) == 0:
        return False
    else: return link_list

# 第一问的函数，不大于limit次转弯的就可以消除
def limit_link(Board, limit):
    link_num = -1
    link_list = []
    while link_num != 0:
        link_num = 0
        patternclass_num = Board.patternclasslist
        for class_num in patternclass_num:
            for i in range(len(class_num) - 1):
                if(i >= len(class_num) - 1):
                    break
                for j in range(i + 1, len(class_num)):
                    if(j >= len(class_num)): # pop出去了一些节点
                        break
                    path = Dot_to_Dot(Board, class_num[i], class_num[j], limit)
                    if path != False:
                        link_list.append(path)
                        link_num += 1
                        Remove(Board, class_num, i, j)
    if len(link_list) == 0:
        return False
    else: return link_list


                    

