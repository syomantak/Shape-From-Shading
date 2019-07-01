
import numpy as np
import csv

p=[]

with open('a.csv','r') as f:
    a = csv.reader(f)
    for x in a:
        p.append(x)

print(p[100][100])

x = open('p.txt','w')

for i in range(200):
    for j in range(200):
        x.write(str(i)+", "+str(j)+", "+p[i][j]+"\n")
