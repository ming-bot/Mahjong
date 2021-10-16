from Board_Pattern import *
import numpy as np

def IsBlocked(Board, corx, cory):
    list_position = (corx + 1) * (Board.column + 2) + (cory + 1)
    if(Board.maplist[list_position] == -1 or Board.maplist[list_position] == 0):
        return True
    else:
        return False

