# Mahjong

本文档记录连连看大作业的完成过程，以日期版本更新迭代。

----

10.26大致完成主体框架，下面依次介绍。

#### Board\_Pattern.py

本代码中主要定义三个基本类：

##### Board类：

参数：

- row：连连看棋盘的行
- column：连连看棋盘的列
- pattern\_class：图案的种类
- pattern\_number：总棋盘上图案数量的一半（这里我规定棋盘上图案是两两存在的）
- map:list存储整个棋盘的状态
- patternclasslist：按图案种类存储的列表，同一种类存储于同一列表

方法：

- Create\_random\_Board：建立一个随机的地图
- Create\_One\_Board：建立一个指定的地图，输入为一个二维列表
- SetPattern将棋盘上某个方块设置为固定值

##### Pattern类：

图案类：用于搜索两个图案之间的最优（最少转向）路径。

参数：

- number：图案编号。0表示空白或者边界，-1表示不可穿过，正常图案编号为1~$pattern\_number$。
- position：记录图案在棋盘中的位置。
- turntimes:转向次数，即在搜素路径的时候，从起点到当前节点所转弯的次数
- cost：代价函数，优先级队列按照代价函数排序，**代价函数=棋盘面积*转弯次数+曼哈顿距离**。
- parent：记录父节点，输出路径的时候需要使用
- direction：表示上一个点到当前点所走的方向，用于计数转弯次数。 1表示向下，-1向上，2向右，-2向左

##### Map类：

与**Board类**类似，用于找到最小的整个棋盘的cost的路径，具体要求可以参照题目文档第二问。



#### basic\_search.py

本代码中主要描述了基本的搜索方法。

- IsNotBlocked：没有阻挡，可以穿过，只存在于pattern_number=0。
- next\_move：返回目前位置下一步可以到的点的坐标。
- cor\_tran：将坐标转换为int型存储，减少比较次数。
- manhadun\_cost：计算两点之间的曼哈顿距离。
- Create\_turntimes：新建一个pattern，并且根据信息将pattern里面的参数赋值
- Remove：消除两个已经连接的图案。
- Zeroturn\_link：零刷函数，不断对棋盘进行零转弯次数的刷，直到棋盘中都不存在零转弯可消除的情况。
- limit\_link：仿照零刷函数，只不过把零刷变成$limit$刷。

最重要的函数**Dot_to_Dot**：返回两个点之间的一条小于limit转弯次数的路径。否则返回False。



#### totalSearch.py

两个方法

- map\_tran：将整个棋盘存储成一个int。
- next\_map：返回目前棋盘的下一步可能变成的棋盘。
- **Leastcost_link**：解决题目中第二部的问题，本质上为一致代价搜索。

