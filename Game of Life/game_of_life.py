from copy import deepcopy
from random import randint
from time import sleep
import os
import shutil

x, y = 44, 60
f = [[randint(0, 5) == 0
for _ in range(y)]
for _ in range(x)]
while True:   
    t = deepcopy(f)
    for i, row in enumerate(f):
        for j, c in enumerate(row):
            l = j-1
            r = (j+1)%y
            u = f[i-1]
            m = f[i]
            b = f[(i+1)%x]
            s = sum((
        u[l], u[j], u[r],
        m[l], m[r],
        b[l], b[j], b[r]))
            if s == 2:
                t[i][j] = c
            elif s == 3:
                t[i][j] = True
            else:
                t[i][j] = False
   # os.system('clear')
    print("\033[0;0H")
    for row in t:
        print(''.join(' X'[c] for c in row))
    f = t
    sleep(.1)
    
    
    
        
        
        
        
