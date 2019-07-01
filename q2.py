from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import csv

s = [0,0,1]
lam = 1
a=200
r=80
rate = 0.1

def avg(p,i,j):
    z = p[i,j+1]+p[i,j-1]+p[i-1,j]+p[i+1,j]
    z = z/4.0
    return z

def R(p,q,i,j):
    z = 1/np.sqrt(p[i,j]**2+q[i,j]**2+1)
    return z

def Rp(p,q,i,j):
    z = -p[i,j]/(np.sqrt(p[i,j]**2+q[i,j]**2+1))**3
    return z

def Rq(p,q,i,j):
    z = -q[i,j]/(np.sqrt(p[i,j]**2+q[i,j]**2+1))**3
    return z

def get_z(i,j,a,r):
    z = np.sqrt(r**2 - (i-a/2)**2 - (j-a/2)**2 )
    return z

img = Image.open('001_nn.png')
e = img.load()

width, height = img.size

p = np.zeros((width,height))
q = np.zeros((width,height))

for i in range(1,width-1):
    for j in range(1,height-1):
        if((r**2-(i-a/2)**2-(j-a/2)**2>0) and (abs(np.sqrt(r**2-(i-a/2)**2-(j-a/2)**2)-53)<2)):
            p[i,j] = 2*(i-a/2)/(1+np.sqrt(r**2-(i-a/2)**2-(j-a/2)**2)/r)
            q[i,j] = 2*(j-a/2)/(1+np.sqrt(r**2-(i-a/2)**2-(j-a/2)**2)/r)

p_t = p
q_t = q


for _ in range(700):
    print("Iteration : "+str(_))
    for i in range(1,width-1):
        for j in range(1,height-1):
            if((i-a/2)**2+(j-a/2)**2<r**2 and (abs(np.sqrt(r**2-(i-a/2)**2-(j-a/2)**2)-53)>=2)):
                p_t[i,j] = avg(p,i,j) + lam*(e[i,j]/255 - R(p,q,i,j))*Rp(p,q,i,j)
                q_t[i,j] = avg(q,i,j) + lam*(e[i,j]/255 - R(p,q,i,j))*Rq(p,q,i,j)
    
    p = p_t
    q = q_t


############ FG to PQ convert

pg = np.zeros((width,height))
qg = np.zeros((width,height))

for i in range(a):
    for j in range(a):
        if((i-a/2)**2+(j-a/2)**2<=(r-3)**2):
            pg[i,j] = 4*p[i,j]/(4 - p[i,j]**2 - q[i,j]**2)
            qg[i,j] = 4*q[i,j]/(4 - p[i,j]**2 - q[i,j]**2)

p = pg
q = qg

############  VECTOR FIELD CONSTRAINT

z = np.zeros((width,height))
z_t = z

for i in range(1,width-1):
    for j in range(1,height-1):
        if((r**2-(i-a/2)**2-(j-a/2)**2>0) and ((i==90) or (i==110) or (j==90) or (j==110))):
            z[i,j] = - get_z(i,j,a,r)
 
z_t = z

for _ in range(1300):
    for i in range(a):
        for j in range(a):
            if((i-a/2)**2+(j-a/2)**2<=r**2):
                if((i!=110) and (j!=110) and (i!=90) and (j!=90)):
                    z_t[i,j] = avg(z,i,j) - rate*(p[i+1,j]-p[i,j]+q[i,j+1]-q[i,j])
    z = z_t

z = 100 - z

with open('a.csv','w') as f:
    ppp = csv.writer(f)
    for g in range(200):
        ppp.writerow(z[g,:])


za = open('res.txt','w')

for i in range(a):
    for j in range(a):
        za.write(str(z[i,j])+" ")
    za.write("\n")

za.close()