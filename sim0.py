
from PIL import Image
import numpy as np
'''
im = Image.new("L",(64,64))
pix = im.load()

for i in range(64):
    for j in range(64):
        pix[i,j]=i+j

im.save('test.png','png')
'''

def e_(x,y,s,r):
    if(r**2-x**2-y**2 > 0):
        t = np.sqrt(r**2-x**2-y**2)
        p = x/t
        q = y/t
        if(-p*s[0]-q*s[1]+s[2]>0):
            e = (-p*s[0]-q*s[1]+s[2])/(np.sqrt(p**2+q**2+1)*np.sqrt((s[0])**2+(s[1])**2+(s[2])**2))
            return 255*e
    return 0

_NOISE_ = 0
a = 200
r = 0.4*a
s = [2,1,1]
n = 255*np.random.normal(0,_NOISE_,(a,a))


im = Image.new("L",(a,a))

pix = im.load()

for i in range(a):
    for j in range(a):
        #temp = int(e_(i-a/2,j-a/2,s,r)+n[i,j])
        temp = int(e_(i-a/2,j-a/2,s,r))
        if(temp>255):
            temp = 255
        if(temp<0):
            temp = 0

        pix[i,j] = temp

im.save('x.png','png')