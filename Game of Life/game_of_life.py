import shutil
from copy import deepcopy
from random import randint
from time import sleep

columns, lines = shutil.get_terminal_size()
field = [[randint(0, 5) == 0 for _ in range(columns)] for _ in range(lines)]
while True:
    tmp = deepcopy(field)
    for row_num, row in enumerate(field):
        for col_num, char in enumerate(row):
            l = col_num - 1
            r = (col_num + 1) % columns
            top = field[row_num - 1]
            middle = field[row_num]
            bottom = field[(row_num + 1) % lines]
            s = sum((
                top[l],
                top[col_num],
                top[r],
                middle[l],
                middle[r],
                bottom[l],
                bottom[col_num],
                bottom[r],
                ))
            if s == 2:
                tmp[row_num][col_num] = char
            elif s == 3:
                tmp[row_num][col_num] = True
            else:
                tmp[row_num][col_num] = False
    print("\033[0;0H")
    for row in tmp:
        print("".join(" X"[c] for c in row))
    field = tmp
    sleep(0.5)
