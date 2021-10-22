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

def Remove(Board, begin, end):
    patternclass = begin.number
    Board.patternclasslist[patternclass - 1].pop(begin)
    Board.patternclasslist[patternclass - 1].pop(end)
    Board[begin.position[0]][begin.position[1]] = 0
    Board[end.position[0]][end.position[1]] = 0

def Dot_to_Dot(Board, begin, end, limit):
    # 初始化队列
    begin.cost = manhadun_cost(begin.position, end.position)
    Unsearch = PriorityQueue(begin)
    Searched = set()
    IsSearch = False
    '''
    将Unsearch队列中的Node取出至Searched，将可能的下一个Node再排入Unsearch
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
        # 可能的新Node
        for vaild_candidate in valid_candidates:
            Next_Node = Create_turntimes(Board, Current_Search, vaild_candidate)
            if(Next_Node.turntimes > limit):
                continue
            if all(Next_Node == end):
                Next_Node.cost = (Board.row + 2) * (Board.column + 2) * Next_Node.turntimes
                print(Next_Node.cost)
                print("预消除两个点为：")
                print(begin, end)
                IsSearch = True
                break

            if((Unsearch.find(Next_Node) or Searched.__contains__(cor_tran(Board, Next_Node.position))) == False):
                Next_Node.cost = (Board.row + 2) * (Board.column + 2) * Next_Node.turntimes + manhadun_cost(Next_Node.position, end.position)
                print(Next_Node.cost)
                print(Next_Node)
                Unsearch.push(Next_Node)
        print("!")
    if IsSearch:
        print("有信息搜索结果为：\n")
        print(Next_Node.path())
    else:
        print('None!Not found!')