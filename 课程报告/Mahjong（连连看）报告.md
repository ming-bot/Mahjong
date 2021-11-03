# Mahjong（连连看）报告

自96 明陈林 2019011457

### 1.前期的思考

在本次大作业开始前，我并没有急于开始写代码，而是前期构想了一下整体的架构。虽然后续仍然增加了一些更改，但是总体来说有一个大致的架构，让我编程的过程变得更加轻松。

##### Board类：

参数：

- $row$：连连看棋盘的行
- $column$：连连看棋盘的列
- $pattern\_class$：图案的种类
- $pattern\_number$：总棋盘上图案数量的一半（这里我规定棋盘上图案是两两存在的）
- $map:list$存储整个棋盘的状态
- $patternclasslist$：按图案种类存储的列表，同一种类存储于同一列表

方法：

- $Create\_random\_Board$：建立一个随机的地图
- $Create\_One\_Board$：建立一个指定的地图，输入为一个二维列表
- $SetPattern$将棋盘上某个方块设置为固定值

这里为什么想要加上$patternclasslist$这个的列表呢，主要是我考虑到连连看这是一个越消越少的过程，如果每次消除都要读取整块棋盘的状态，那么其实对于稀疏矩阵来讲，其大部分的地方就会多余判断的过程。而我直接在$patternclasslist$里面进行操作，就避免了多余的搜索。



##### Pattern类：

图案类：用于搜索两个图案之间的最优（最少转向）路径。

参数：

- $number$：图案编号。0表示空白或者边界，-1表示不可穿过，正常图案编号为1~$pattern\_number$。
- $position$：记录图案在棋盘中的位置。
- $turntimes:$转向次数，即在搜素路径的时候，从起点到当前节点所转弯的次数
- $cost$：代价函数，优先级队列按照代价函数排序，**代价函数=棋盘面积*转弯次数+曼哈顿距离**。
- $parent$：记录父节点，输出路径的时候需要使用
- $direction$：表示上一个点到当前点所走的方向，用于计数转弯次数。 1表示向下，-1向上，2向右，-2向左

这里说明一下$cost$我的设计，首先明确本次的代价是转弯的次数，为了使用起始点和目标点的坐标信息，来加速搜索过程，很容易想到利用曼哈顿距离来优化搜索时间。但是如果仅仅是拿曼哈顿距离+转弯次数，会出现下图的问题：

![pattern_cost](D:\Tsinghua\Mahjong\课程报告\pattern_cost.jpg)

虽然两点中间的转弯次数为3，但是由于曼哈顿距离短，仍然会导致中间连线的优先级高于转弯次数为2，但是曼哈顿距离会很大的路径。总结：转弯次数的比重应该远大于曼哈顿距离，使得即使曼哈顿距离达到最大所造成的代价仍然比转弯一次的代价小。所以我在转弯次数前乘上了一个系数为棋盘的面积，解决了这个问题。

转弯方向这边，如果使用[[1,0],[-1,0],[0,1],[0,-1]]记录转弯方向，会在后期有较多的比较代码，于是我采用

```python
Direction = cor[0] - pattern.position[0] + 2 * (cor[1] - pattern.position[1]) # 1表示向下，-1向上，2向右，-2向左
```

一行代码解决了方向问题。



想清楚了这些，我就开始了主体程序的编写。有了前期的思考，基础代码就好写很多了。



### 2.主要算法的说明

一些基础方法的功能：

- $IsNotBlocked$：没有阻挡，可以穿过，只存在于$pattern\_number=0$。
- $next\_move$：返回目前位置下一步可以到的点的坐标。
- $cor\_tran$将坐标转换为int型存储，减少比较次数。
- $manhadun\_cost$：计算两点之间的曼哈顿距离。
- $Create\_turntimes$：新建一个pattern，并且根据信息将pattern里面的参数赋值
- $Remove$：消除两个已经连接的图案。

#### 2.1 两点之间搜索函数

```python
# Dot_to_Dot函数负责测定两点之间在不超过limit次转弯的基础上能不能消除，若能返回路径，不能就返回False
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
                IsSearch = True
                break

            if((Unsearch.find(Next_Node) or Searched.__contains__(cor_tran(Board, Next_Node.position))) == False):
                Next_Node.cost = (Board.row + 2) * (Board.column + 2) * Next_Node.turntimes + manhadun_cost(Next_Node.position, end.position)
                Unsearch.push(Next_Node)
    if IsSearch:
        return (Next_Node.path())
    else:
        return False
```

这里就是一个A*的搜索，启发函数为**棋盘面积 x 转弯次数+曼哈顿距离**，按照第一部分的说明，可以契合题目要求。

#### 2.2 全局转弯次数最小的算法

我的第一个想法是：每次都找棋盘上面的最小转弯次数能消除的点进行消除。但是这个贪心算法的问题是显而易见的，局部的最优解并不一定是全局的最优解。存在一些耦合的节点对，其消除的次序会影响整体的代价。基于此，就一定需要回溯的算法，或者将所有的节点代价都进行消除排进队列中，代价小的优先出列，这样才一定能保证整体的代价最小。

进一步思考，如果每次都把转弯次数很大的点排入队列中，整体上还是会加入很多的无用的节点，后来经过进一步的实验，我发现，最小代价消除的点的顺序才是影响问题的关键。只需要将目前棋盘的最小消除的对全部分开消除，将下一步的棋盘排进优先级队列，就可以得到最终较好的结果。

由于需要记录每一步的棋盘，所以我在基础类的上面又扩充了map类，其基本与Board类类似，用于记录每一步的棋盘状态。

下面就是最终的全局最小转弯次数的代码：

```python
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
```

这里说明启发函数。首先必须要有转弯次数，另一项为预期的代价。比如假设某一图案同行同列都没有相同图案，那么消除它至少需要转弯1次，所以就可以将它的预期代价置为0.5（因为对称，会存在另一个图案，连接使得转弯次数至少为1。

为了进一步加速搜索速度，我们还可以加入目前棋盘上面未消除的对数。但是问题是，即使目前棋盘上面已经全部消除完毕，但是转弯次数大的仍然要处于优先级队列的后端。极端情况为：少一级转弯次数但是全部未消，参照**2.1**中的想法，将前面的代价乘上$k$（是初始化的图案对数），这样子就保证了A*的一致性和完备性。



