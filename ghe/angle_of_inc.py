import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.colors as colors

a = 1
b = 0.88
x = np.linspace(-a, a, num=600)
fi0 = lambda x: np.arctan( ((a*a)/(b))*np.sqrt(1/(x*x)-1/(a*a)))/(np.pi/180) 	# sprawdzic skalowanie
fiN = lambda x: np.arctan( b*np.sqrt(1/(x*x)-1/(a*a)))/(np.pi/180)				# sprawdzic skalowanie

fi0L = map(fi0, x)
fiNL = map(fiN, x)
fiDiff = np.subtract(fi0L,fiNL)
print max(fiDiff)
# print max( (v, i) for i, v in enumerate(fiDiff) )[1]
i = max( (v, i) for i, v in enumerate(fiDiff) )[1]
v = max( (v, i) for i, v in enumerate(fiDiff) )[0]
print "Maksymalna roznica dla: ", fi0L[i], " stopni"
print "Wynosi ona: ", v, " stopni"


def find_nearest(array, value):
    n = [abs(i-value) for i in array]
    idx = n.index(min(n))
    return array[idx], idx

angle1 = 60
angle2 = 75
v1, i1 =  find_nearest(fiNL, angle1)
v2, i2 =  find_nearest(fiNL, angle2)
print "kat najblizszy ", angle1, " to ", v1, "\trzeczywisty kat padania to: ", fi0L[i1]
print "kat najblizszy ", angle2, " to ", v2, "\trzeczywisty kat padania to: ", fi0L[i2]

ax1 = plt.subplot(3,1,1)
ax1.plot(x, fiNL)
ax1.plot(x, fi0L)
ax2 = plt.subplot(3,1,2)
ax2.plot(fi0L, fiNL)
ax2.plot(fi0L, fi0L)
ax3 = plt.subplot(3,1,3)
ax3.plot(fi0L, fiDiff)
# print len(x)
# print fi0L[0], fiNL[0]
# print fi0L[len(x)-1], fiNL[len(x)-1]
# print max(fi0L), max(fiNL)


plt.show() 
plt.close()