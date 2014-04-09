import os
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import re as re
import struct
import time

if __name__ == "__main__":
	filename = 'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\semanti\\500nm.txt'
	with open(filename, 'rb') as f:
		i=0
		freq=[]
		amp=[]
		i = 0
		print f.readline()
		with open(filename, 'rb') as f:
			while True:
				i += 1
				a = re.split('[\t, \n, \r]', f.readline())

				if len(a)<2:
					break # EOF
				freq.append(float(a[0] ))
				k = a[1]
				amp.append(float(a[1]+'.'+a[2])) # polski format
				#amp.append(float(a[1]))
	print "number of points from Semanti measurments: ", i

	plt.plot(freq,amp,color="g", label=r'Semanti', alpha=0.5)
	plt.show()
	fig = plt.gcf()
	plt.close()