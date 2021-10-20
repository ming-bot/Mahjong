from Board_Pattern import *
import numpy as np

if __name__ == "__main__":
    # m = input("请输入地图的长：")
    # n = input("请输入地图的宽：")
    # p = input("请输入图案的种类：")
    # k = input("请输入图案的数目：")  # 这里还要处理输入数据是否合法
    board = Board(3, 3, 3, 3)
    mymap = np.array([[0,3,3],[1,1,0],[2,0,2]])
    board.Create_One_Board(mymap)
    print(board.map)
    