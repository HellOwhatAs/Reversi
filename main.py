from typing import List, Tuple, Iterable
from itertools import product
from copy import deepcopy
from browser import document, window, alert
from browser.html import DIV

class Solution:
    def directed_update(self, it: Iterable[Tuple[int, int]]):
        if self.round:
            childs = []
            for x, y in it:
                if self.chessboard[x][y] == 'X': childs.append((x, y))
                elif self.chessboard[x][y] == '.': break
                else:
                    for a, b in childs: self.chessboard[a][b] = 'O'
                    return childs
            return []
        
        childs = []
        for x, y in it:
            if self.chessboard[x][y] == 'O': childs.append((x, y))
            elif self.chessboard[x][y] == '.': break
            else:
                for a, b in childs: self.chessboard[a][b] = 'X'
                return childs
        return []

    def update(self, i: int, j: int):
        all_childs = []
        all_childs.extend(self.directed_update(((_, j) for _ in range(i - 1, -1, -1))))
        all_childs.extend(self.directed_update(((_, j) for _ in range(i + 1, self.m))))
        all_childs.extend(self.directed_update(((i, _) for _ in range(j - 1, -1, -1))))
        all_childs.extend(self.directed_update(((i, _) for _ in range(j + 1, self.n))))
        all_childs.extend(self.directed_update(zip(range(i - 1, -1, -1), range(j - 1, -1, -1))))
        all_childs.extend(self.directed_update(zip(range(i + 1, self.m), range(j - 1, -1, -1))))
        all_childs.extend(self.directed_update(zip(range(i + 1, self.m), range(j + 1, self.n))))
        all_childs.extend(self.directed_update(zip(range(i - 1, -1, -1), range(j + 1, self.n))))
        for a, b in all_childs:
            self.update(a, b)
    
    def try_update(self, i, j):
        old_chessboard = deepcopy(self.chessboard)
        self.chessboard[i][j] = 'O' if self.round else 'X'
        self.update(i, j)
        able = sum(i.count('X' if self.round else 'O') for i in old_chessboard) - sum(i.count('X' if self.round else 'O') for i in self.chessboard)
        new_chessboard = self.chessboard
        self.chessboard = old_chessboard
        return new_chessboard, able
    
    def myupdate(self, i, j):
        if self.chessboard[i][j] != '.': return
        new_chessboard, able = self.try_update(i, j)
        if not able: return
        self.chessboard = new_chessboard
        self.round = not self.round
        if self.round:
            document.documentElement.style.setProperty('--cursor', "url(./white.cur)")
        else:
            document.documentElement.style.setProperty('--cursor', "url(./black.cur)")
        self.render()

    def render(self):
        for i in range(self.m):
            for j in range(self.n):
                items[i][j].text = ''
                if self.chessboard[i][j] != '.': able = 0
                else: _, able = self.try_update(i, j)
                items[i][j].style = "background-color: {};".format("black" if self.chessboard[i][j] == 'X' else (
                    "white" if self.chessboard[i][j] == 'O' else "lightgray"))
                if able:
                    items[i][j].text = str(able)
                    items[i][j].style = "border-color: green;"
    
    def __init__(self, chessboard):
        self.m, self.n = len(chessboard), len(chessboard[0])
        self.chessboard = chessboard
        self.round = False

n = window.location.search[1:]
if not n: n = 10
row_num = col_num = int(n)
document.documentElement.style.setProperty('--cols', col_num)
chessboard = Solution([['.' for _ in range(col_num)] for _ in range(row_num)])
chessboard.chessboard[row_num // 2][col_num // 2] = 'X'
chessboard.chessboard[row_num // 2 - 1][col_num // 2 - 1] = 'X'
chessboard.chessboard[row_num // 2 - 1][col_num // 2] = 'O'
chessboard.chessboard[row_num // 2][col_num // 2 - 1] = 'O'
container = document.getElementById("grid-container")
items = []
for i in range(row_num):
    items.append([])
    for j in range(col_num):
        item = DIV(Class="grid-item", style="background-color: lightgray;")
        item.bind("click", eval("lambda e: chessboard.myupdate({}, {})".format(i, j)))
        container <= item
        items[-1].append(item)
chessboard.render()