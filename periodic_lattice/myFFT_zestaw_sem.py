import os
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import re as re
import struct
import time

from numbapro.cudalib import cufft
from numbapro import cuda
from timeit import default_timer as timer

def getData(filename, w0t, wft, t0t, tkt):
	print filename
	# t0t = 10e-09
	# tkt = 30e-09
	a = ""
	with open(filename, 'rb') as f:
		# t
		print f.readline()
		i=0
		print "reading file..."
		times2Tr = []
		m2Tr_z = []
		m2Tr_x = []
		m2Tr_y = []
		b2Tr = []
		while True:
			a = re.split(r'\t+', f.readline())
			if len(a)<3:
				break # EOF
			times2Tr.append(float(a[0]))
			# m2Tr.append(np.sqrt(float(a[1])**2 + float(a[2])**2) )
			m2Tr_z.append(float(a[3]))
			m2Tr_x.append(float(a[1]))
			m2Tr_y.append(float(a[2]))
			# m2Tr_z.append( np.sqrt( (float(a[1])**2)+(float(a[2])**2)+(float(a[3])**2)  ) ) 
			# m2Tr_z.append( np.sqrt( float(a[1])**2+float(a[2])**2+float(a[3])**2) ) 
			b2Tr.append(float(a[4]))
			if float(a[0]) > tkt:
				break
			i+=1
			if i%100000==0:
				print i
			# if i > 20: break
	print "Number of points to process"
	print len(times2Tr), len(m2Tr_z)

	
	t0 = min( range(len(times2Tr)), key=lambda i: abs(times2Tr[i]-t0t))
	tk = min( range(len(times2Tr)), key=lambda i: abs(times2Tr[i]-tkt))

	print "FFT..."
	print (time.strftime("%I:%M:%S"))
	ts = timer()
	dt = 1e-13 # MaxDt
	print "x..."
	mi_fitFFT_x = np.fft.fft(m2Tr_x[0:tk])
	print "y..."
	mi_fitFFT_y = np.fft.fft(m2Tr_y[0:tk])
	print "z..."
	mi_fitFFT_z = np.fft.fft(m2Tr_z[0:tk])
	bi_fitFFT = np.fft.fft(b2Tr)
	freq = np.fft.fftfreq(len(times2Tr[0:tk]), dt)
	te = timer()
	print('CPU: %.2fs' % (te - ts))

	w0t = 0.25e09 # 5.8e09
	w0 = min( range(len(freq)), key=lambda i: abs(freq[i]-w0t))
	# print w0

	wft = 22.5e09	# = 6e08 = 60e09
	wf = min( range(len(freq)), key=lambda i: abs(freq[i]-wft))
	# print wf
	freqc = []
	mi_fitFFT_xc = []
	mi_fitFFT_yc = []
	mi_fitFFT_zc = []

	try:
		print "2nd FFT..."
		print (time.strftime("%I:%M:%S"))
		ts = timer()
		print "x..."
		li = np.array(m2Tr_x[t0:tk])
		print "dt = ", ( timer()-ts ), len(li)
		mi_fitFFT_xc = np.fft.fft(li)
		print "y..."
		mi_fitFFT_yc = np.fft.fft(m2Tr_y[t0:tk])
		print "z..."	
		mi_fitFFT_zc = np.fft.fft(m2Tr_z[t0:tk])
		
		freqc = np.fft.fftfreq(len(times2Tr[t0:tk]), dt)
		te = timer()
		print('CPU: %.2fs' % (te - ts))
		w0 = min( range(len(freqc)), key=lambda i: abs(freqc[i]-w0t))
		wf = min( range(len(freqc)), key=lambda i: abs(freqc[i]-wft))
	except ValueError:
		print "Error: ", ValueError

	print "done."
	return [freqc[w0:wf], np.abs(mi_fitFFT_xc[w0:wf]), np.abs(mi_fitFFT_yc[w0:wf]), np.abs(mi_fitFFT_zc[w0:wf])]

if __name__ == "__main__":
	w0t = 0.5e09 # 5.8e09
	wft = 22.5e09	# = 6e08 = 60e09
	t0t = 10e-09
	tkt = 30e-09
	li_7nm = [  'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\200nm\\200nm_Ha_0.3_r_7.out\\table.txt', \
				'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\300nm\\300nm_Ha_0.3_r_7.out\\table.txt',\
				'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\400nm\\400nm_Ha_0.3_r_7.0.out\\table.txt', \
				'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\500nm\\500nm_Ha_0.3_r_7.out\\table.txt']
	
	li_8_5nm = ['C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\200nm\\200nm_Ha_0.3_r_8.5.out\\table.txt', \
				'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\300nm\\300nm_Ha_0.3_r_8.5.out\\table.txt', \
				'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\400nm\\400nm_Ha_0.3_r_8.5.out\\table.txt', \
				'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\300nm\\300nm_Ha_0.3_r_8.5.out\\table.txt']		
	
	li_9nm = [  'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\200nm\\200nm_Ha_0.3_r_9.0.out\\table.txt', \
				'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\300nm\\300nm_Ha_0.3_r_9.0.out\\table.txt', \
				'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\400nm\\400nm_Ha_0.3_r_9.0.out\\table.txt', \
				'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\500nm\\500nm_Ha_0.3_r_9.out\\table.txt']		

	li_11nm = [ 'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\200nm\\200nm_Ha_0.3_r_11.out\\table.txt', \
				'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\300nm\\300nm_Ha_0.3_r_11.out\\table.txt', \
				'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\400nm\\400nm_Ha_0.3_r_11.0.out\\table.txt', \
				'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\500nm\\500nm_Ha_0.3_r_11.out\\table.txt']	

	li_8_5nm_d=['C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\200nm\\deep_200nm_Ha_0.3_r_8.5.out\\table.txt', \
				'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\300nm\\deep_300nm_Ha_0.3_r_8.5.out\\table.txt', \
				'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\400nm\\deep_400nm_Ha_0.3_r_8.5.out\\table.txt', \
				'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\500nm\\deep_500nm_Ha_0.3_r_8.5.out\\table.txt']	
		
	fileLi = [ 'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\semanti\\200nm.txt',\
				'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\semanti\\300nm.txt',\
				'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\semanti\\400nm.txt',\
				'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\semanti\\500nm.txt' ]


	
	fLi = li_7nm
	title = r'$dr=7nm$'
	titlesLi = [r'$a=200nm$', r'$a=300nm$', r'$a=400nm$', r'$a=500nm$']
	print titlesLi
	print range(len(fileLi))
	axs = []
	for id in range(len(fileLi)):
		axs.append(plt.subplot(4, 1, id))
	for id in range(len(fileLi)):
		# with open(fileLi[id], 'rb') as f:
		i=0
		freq=[]
		amp=[]
		i = 0
		with open(fileLi[id], 'rb') as f:
			while True:
				i += 1
				a = re.split('[\t, \n, \r]', f.readline())
				if len(a)<2:
					break # EOF
				freq.append(float(a[0]))
				amp.append(float(a[1]+'.'+a[2])) # convert pol format of numb
				#amp.append(float(a[1]))
		print "number of points from Semanti measurments: ", i
		w00 = 0 # 5.8e09
		w0i = min( range(len(freq)), key=lambda i: abs(freq[i]-w00))
		freq=freq[w0i:]
		amp=amp[w0i:]
		[f, mx, my, mz] = getData(fLi[id], w0t, wft, t0t, tkt)
		max_amp = max(amp)
		max_mx= max(mx)
		coef = max_mx/max_amp
		amp1=map(lambda x: x*coef, amp)
		# p500 = plt.subplot(4, 1, id)
		axs[id].plot(freq,amp1,color="g", label=r'Semanti', lw=2)
		axs[id].fill_between(freq,0, amp1,color="g", label=r'Semanti', alpha=0.33)
		axs[id].plot(f, mx,color="b", label=r'$m_{x}$', lw=2)
		axs[id].fill_between(f, 0, mx,color="b", label=r'$m_{x}$', alpha=0.33)
		axs[id].plot(f, mz,color="r", label=r'$m_{z}$', lw=2)
		axs[id].fill_between(f, 0, mz,color="r", label=r'$m_{z}$', alpha=0.33)
		axs[id].set_ylabel(titlesLi[id], fontsize=16)
		axs[id].set_xlabel(r'$\nu$ [Hz]')
		axs[id].legend(ncol=1, fancybox=True, shadow=True)

	plt.suptitle(title, fontsize=20)
	plt.show()
	fig = plt.gcf()
	plt.close()