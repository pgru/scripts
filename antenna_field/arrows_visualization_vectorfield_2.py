from pylab import *
from numpy import ma

X,Y = meshgrid( arange(0,2*pi,.2),arange(0,2*pi,.2) )
U = 1
V = sin(Y)


#4
figure()
M = sqrt(pow(U, 2) + pow(V, 2))
print X
print len(X), len(X[0])
Q = quiver( X, Y, U, V, M, units='x', pivot='tip', width=0.022, scale=1/0.15)
# qk = quiverkey(Q, 0.9, 1.05, 1, r'$1 \frac{m}{s}$',
                            # labelpos='E',
                            # fontproperties={'weight': 'bold'})
plot(X, Y, 'k.')
axis([-1, 7, -1, 7])
title("scales with x view; pivot='tip'")

show()