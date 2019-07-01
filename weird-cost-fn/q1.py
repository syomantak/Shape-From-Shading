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
    z = p[i,j+1]+p[i+1,j]+p[i-1,j]+p[i,j-1]+(p[i+1,j+1]+p[i-1,j-1]+p[i+1,j-1]+p[i-1,j+1])*0.5
    z = z/6
    return z

def R(p,q,i,j,s):
    mods = np.sqrt(s[0]**2 + s[1]**2 + s[2]**2)
    modn = np.sqrt(p[i,j]**2 + q[i,j]**2 + 1)

    num = p[i,j]*s[0] + q[i,j]*s[1] + s[2]

    z = num/(mods*modn)
    return z

def Rp(p,q,i,j,s):
    mods = np.sqrt(s[0]**2 + s[1]**2 + s[2]**2)
    modn = np.sqrt(p[i,j]**2 + q[i,j]**2 + 1)

    num = p[i,j]*s[0] + q[i,j]*s[1] + s[2]

    z = (s[0]*(modn**2) - p[i,j]*num)/(mods*(modn**3))
    
    return z

def Rq(p,q,i,j,s):
    mods = np.sqrt(s[0]**2 + s[1]**2 + s[2]**2)
    modn = np.sqrt(p[i,j]**2 + q[i,j]**2 + 1)

    num = p[i,j]*s[0] + q[i,j]*s[1] + s[2]

    z = (s[1]*(modn**2) - q[i,j]*num)/(mods*(modn**3))
    
    return z

def get_z(i,j,a,r):
    z = np.sqrt(r**2 - (i-a/2)**2 - (j-a/2)**2 )
    return z

img = Image.open('001_01n.png')
e = img.load()

width, height = img.size

p = np.zeros((width,height))
q = np.zeros((width,height))

for i in range(1,width-1):
    for j in range(1,height-1):
        if((r**2-(i-a/2)**2-(j-a/2)**2>0) and (abs(np.sqrt(r**2-(i-a/2)**2-(j-a/2)**2)-53)<2)):
            p[i,j] = (i-a/2)/np.sqrt(r**2-(i-a/2)**2-(j-a/2)**2)
            q[i,j] = (j-a/2)/np.sqrt(r**2-(i-a/2)**2-(j-a/2)**2)

p_t = p
q_t = q


for _ in range(1000):
    print("Iteration : "+str(_))
    for i in range(2,width-2):
        for j in range(2,height-2):
            if((i-a/2)**2+(j-a/2)**2<(r-5)**2 and (abs(np.sqrt(r**2-(i-a/2)**2-(j-a/2)**2)-53)>=2)):
                p_t[i,j] = avg(p,i,j) + lam*(e[i,j]/255 - R(p,q,i,j,s))*Rp(p,q,i,j,s)
                q_t[i,j] = avg(q,i,j) + lam*(e[i,j]/255 - R(p,q,i,j,s))*Rq(p,q,i,j,s)
    
    p = p_t
    q = q_t


############ GROUND TRUTH GENERATION

z = np.zeros((width,height))
z_t = z

for i in range(1,width-1):
    for j in range(1,height-1):
        if((r**2-(i-a/2)**2-(j-a/2)**2>0) and ((i==90) or (i==110) or (j==90) or (j==110))):
            z[i,j] = - get_z(i,j,a,r)
 
z_t = z

for _ in range(1100):
    for i in range(a):
        for j in range(a):
            if((i-a/2)**2+(j-a/2)**2<=(r-5)**2):
                if((i!=110) and (j!=110) and (i!=90) and (j!=90)):
                    z_t[i,j] = avg(z,i,j) - rate*(p[i+1,j]-p[i,j]+q[i,j+1]-q[i,j])
    z = z_t

z = - z

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