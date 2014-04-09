__author__ = 'TaytaInti'

import os
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import pylab as pylab

if __name__ == "__main__":
	c = 1e-05

	w = 5e-0*c
	h = 5e-0*c
	l = 20e-0*c
	[dx, dy, dz] = [1e-0*c,1e-0*c,1e-0*c] 
	# x = np.linspace(-1, 1, num=3)
	# y = np.linspace(w/2, 10*w, num=20)
	# z = np.linspace(0, 3, num=3)
	# xiLi = np.linspace(-50, 51, num=100)
	# yiLi = np.linspace(-w/2, w/2, num=10)
	# ziLi = np.linspace(-h/2, h/2, num=6)

	x = np.arange(-dx, 2*dx, dx)
	y = np.arange(w/2+w/2, w/2+20*dy, dy)
	z = np.arange(-2*dy-h/2, h/2+3*dz, dz)

	# print np.meshgrid( np.arange(-1, 1.1, 01),np.arange(0, 5, 1), np.arange(-5, -2, 1) )
	# x, y, z = np.meshgrid( np.arange(-1, 1.1, dx),np.arange(w/2, 20, dy), np.arange(-h/2, h/2+2*dz, dz) )

	xiLi = np.arange(-l/2, l/2+2*dx,)
	yiLi = np.arange(-w/2, w/2, dy)
	ziLi = np.arange(-h/2, h/2+dz, dz)
	print len(x)
	print len(y)
	print len(z)
	A = np.zeros((len(x),len(y), len(z) ))
	for i in range(len(x)):
		for j in range(len(y)):
			for k in range(len(z)):
				At = 0
				for xi in xiLi:
					for yi in yiLi:
						for zi in ziLi:
							At += 1/np.sqrt( (x[i]-xi)**2 + (y[j]-yi)**2 + (z[k]-zi)**2 )
				A[i][j][k]= At
			print j, len(y)
	print "A: ", len(A[:,:,:]), len(A[0,:,:]), len(A[0,0,:])
	plt.figure()
	axA = plt.subplot(141)
	axA.matshow(A[1,:,:])
	
	By = np.zeros((len(x),(len(y)-1), (len(z)-1) ))
	Bz = np.zeros((len(x),(len(y)-1), (len(z)-1) ))
	Bm = np.zeros((len(x),(len(y)-1), (len(z)-1) ))
	for i in range(len(x)):
		for j in range(len(y)-1):
			for k in range(len(z)-1):
				By[i][j][k] =  (A[i,j,k+1]-A[i,j,k])/dz
				Bz[i][j][k] = -(A[i,j+1,k]-A[i,j,k])/dy
				Bm[i][j][k] = np.sqrt( By[i][j][k]*By[i][j][k]+ Bz[i][j][k]*Bz[i][j][k] )

	
	axBy = plt.subplot(142)
	axBy.matshow(By[1,:,:])
	axBz = plt.subplot(143)
	axBz.matshow(Bz[1,:,:])
	axBm = plt.subplot(144)
	axBm.matshow(Bm[1,:,:])
	# plt.show()
	# X,Y = np.meshgrid( np.arange(0,2*np.pi,.2),np.arange(0,2*np.pi,.5) )
	Y,Z = np.meshgrid( y[0:len(y)-1], z[0:len(z)-1] )
	# U = np.cos(X)
	# V = np.sin(Y)
	# print X
	# print Y
	# X = y
	# Y = z
	# U = By
	# V = Bz
	#4
	print "======"
	print len(x), len(y), len(z)
	# print x
	# print y
	print Y
	print len(Y), len(Y[0])
	print len(By[1,:,:])
	# print len(y), len(By), len(By[0,:,:]), len(By[0,0,:])
	# print len(z), len(Bz)
	# print len(x)
	plt.figure()
	M = np.sqrt(pow(By[1,:,:], 2) + pow(Bz[1,:,:], 2))
	mv= max( [max(x) for x in M ] )
	print "mv: ", mv
	Q = pylab.quiver(Bz[1,:,:]/mv, By[1,:,:]/mv, pivot='mid', color='r')

	plt.figure()
	print "leny: ", len(y[0:(len(y)-1)])
	print "lenB: ", len( Bz[1,:,int(len(z)/2)] )
	print int( len(x)/2 )
	a = []
	for i in range(len(y)-1):
		a.append(Bz[1,i,int(len(z)/2)])
	plt.plot(y[0:(len(y)-1)], Bz[1,:,int(len(z)/2)])
	# plt.plot(y[0:(len(y)-1)], a)
	# qk = pylab.quiverkey(Q, 0.9, 1.05, 1, r'$1 \frac{m}{s}$',
	#                             labelpos='E',
	#                             fontproperties={'weight': 'bold'})
	# plt.plot(X, Y, 'k.')
	# plt.axis([-1, 7, -1, 7])
	# plt.title("scales with x view; pivot='tip'")

	# plt.show()

	# colorsLi = ["b", "g", "r", "c", "m", "y", "k"]	
	# plt.figure()
	# ax1 = plt.subplot(411)
	# for i in range(len(z)):
	# 	ax1.plot(x, A[:,2,i], label=str(z[i]) )
	# # ax1.plot(y, A[1])
	# ax1.legend(fancybox=True, shadow=True)
	# ax1.set_ylabel("Ax")
	# ax1.set_xlabel("y")

	# ax2 = plt.subplot(412)
	# for i in range(len( By[0,0,:] )):
	# 	ax2.plot(y[0:(len(y)-1)], By[1,:,i], label=str(z[i]) )
	# ax2.set_ylabel("By")
	# ax2.set_xlabel("y")
	# ax2.legend(fancybox=True, shadow=True)

	# ax3 = plt.subplot(413)
	# for i in range(len( Bz[0,0,:] )):
	# 	ax3.plot(y[0:(len(y)-1)], Bz[1,:,i], label=str(z[i]) )
	# ax3.set_ylabel("Bz")
	# ax3.set_xlabel("y")
	# ax3.legend(fancybox=True, shadow=True)

	# ax4 = plt.subplot(414)
	# for i in range(len( Bm[0,0,:] )):
	# 	ax4.plot(y[0:(len(y)-1)], Bm[1,:,i], label=str(z[i]) )
	# ax4.set_ylabel("|B|")
	# ax4.set_xlabel("y")
	# ax4.legend(fancybox=True, shadow=True)

	plt.show()
	plt.close()

	f = open("pole.txt", 'w')
	for i in range(len(x)):
		for j in range(len(y)-1):
			for k in range(len(z)-1):
				s = str(x[i]) + "\t" + str(y[j]) + "\t" + str(z[k]) + "\t" + str(0) + "\t" + str(By[i,j,k]) + "\t" + str(Bz[i,j,k]) + "\n" 
				f.write(s)
    #f.write("\n#End")
	f.close()


