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

def getData():
	# strs = "foo\tbar\t\tspam"
	# print re.split(r'\t+', strs)
	# filename = 'C:\\Users\\Pawel\\workspace\\mumax3\\hole_angle.out\\table.txt'
	# filename = 'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\a_500nm_0deg\\a_500nm_0deg.out\\table.txt'
	# filename = 'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\9hols\\25holes.out\\table.txt'
	# filename = 'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\toCheck\\sim1_tst.out\\table.txt'
	filename = 'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\toCheck\\sim1_tst.out\\table.txt'
	bulk_fn = 'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\toCheck\\sim1_bulk.out\\table.txt'
	print filename
	print bulk_fn

	a = ""
	with open(bulk_fn, 'rb') as f:
		# t
		print f.readline()
		# while not "#Data:" in a:
		# 	a = f.readline().strip()

		i=0
		print "reading bulk file..."
		times2Tr_bulk = []
		m2Tr_bulk = []
		b2Tr_bulk = []
		while True:
			a = re.split(r'\t+', f.readline())
			# a = .strip('\t\n\r')
			# print type(a)
			# print a, len(a)
			# print a[0], a[1]
			if len(a)<3:
				break # EOF
			times2Tr_bulk.append(float(a[0]))
			# m2Tr.append(np.sqrt(float(a[1])**2 + float(a[2])**2) )
			m2Tr_bulk.append(float(a[3]))
			# m2Tr.append( np.sqrt( (float(a[1])**2)+(float(a[2])**2)+(float(a[3])**2)  ) ) 
			# m2Tr.append( np.sqrt( float(a[1])**2+float(a[2])**2+float(a[3])**2) ) 
			b2Tr_bulk.append(float(a[4]))
			i+=1
			if i%100000==0:
				print i


	a = ""
	with open(filename, 'rb') as f:
		# t
		print f.readline()
		# while not "#Data:" in a:
		# 	a = f.readline().strip()

		i=0
		print "reading file..."
		times2Tr = []
		m2Tr = []
		b2Tr = []
		while True:
			a = re.split(r'\t+', f.readline())
			# a = .strip('\t\n\r')
			# print type(a)
			# print a, len(a)
			# print a[0], a[1]
			if len(a)<3:
				break # EOF
			times2Tr.append(float(a[0]))
			# m2Tr.append(np.sqrt(float(a[1])**2 + float(a[2])**2) )
			m2Tr.append(float(a[3]))
			# m2Tr.append( np.sqrt( (float(a[1])**2)+(float(a[2])**2)+(float(a[3])**2)  ) ) 
			# m2Tr.append( np.sqrt( float(a[1])**2+float(a[2])**2+float(a[3])**2) ) 
			b2Tr.append(float(a[4]))
			i+=1
			if i%100000==0:
				print i
			# if i > 20: break
	print "Number of points to process"
	print len(times2Tr), len(m2Tr)
	

	print "FFT bulk..."

	print (time.strftime("%I:%M:%S"))
	ts = timer()
	dt = 2.5e-14 # MaxDt
	mi_fitFFT_bulk = np.fft.fft(m2Tr_bulk)
	bi_fitFFT_bulk = np.fft.fft(b2Tr_bulk)
	freq_bulk = np.fft.fftfreq(len(times2Tr_bulk), dt)
	te = timer()
	print('CPU bulk: %.2fs' % (te - ts))

	print "FFT..."

	print (time.strftime("%I:%M:%S"))
	ts = timer()
	dt = 2.5e-14 # MaxDt
	mi_fitFFT = np.fft.fft(m2Tr)
	bi_fitFFT = np.fft.fft(b2Tr)
	freq = np.fft.fftfreq(len(times2Tr), dt)
	te = timer()
	print('CPU: %.2fs' % (te - ts))

	# print len(freq), max(freq), min(freq)

	w0t = 3.0e09 # 5.8e09
	w0 = min( range(len(freq)), key=lambda i: abs(freq[i]-w0t))
	# print w0

	wft = 40e09	# = 6e08 = 60e09
	wf = min( range(len(freq)), key=lambda i: abs(freq[i]-wft))
	# print wf

	
	# print t0, type(t0), len(times2Tr)
	# print times2Tr[t0]

	# d =  [] #cuda.to_device( cufftComplex, stream=stream1 )
	# ts = timer()
	# yi_fitFFT = cufft.fft(amp2Tr, out=d)
	# yi_fit_freq = cufft.fftfreq(len(times2Tr), dt)
	# te = timer()
	# print('GPU: %.2fs' % (te - ts))


	btplot = plt.subplot(321)
	btplot.plot(times2Tr, b2Tr,color="g")
	btplot.set_title("B_ext", fontsize=14)
	btplot.set_xlabel("time [s]")
	btplot.set_ylabel("B amp [T]")

	bplot = plt.subplot(322)
	bplot.plot(freq[w0:wf], np.abs(bi_fitFFT[w0:wf]),color="g")
	bplot.set_title("FFT of B_ext", fontsize=14)
	bplot.set_xlabel("omega [Hz]")
	bplot.set_ylabel("B amp [T]")

	mtplot = plt.subplot(323)
	mtplot.plot(times2Tr, m2Tr,color="b")
	mtplot.plot(times2Tr_bulk, m2Tr_bulk, color='r')
	mtplot.set_title("m", fontsize=14)
	mtplot.set_xlabel("time [s]")
	mtplot.set_ylabel("m amp")


	mplot = plt.subplot(324)
	mplot.plot(freq[w0:wf], np.abs(mi_fitFFT[w0:wf]),color="b")
	mplot.plot(freq_bulk[w0:wf], np.abs(mi_fitFFT_bulk[w0:wf]),color="r")
	mplot.set_title("FFT of m", fontsize=14)
	mplot.set_xlabel("omega [Hz]")
	mplot.set_ylabel("m amp")
	
	t0t = 1.12e-09
	t0 = min( range(len(times2Tr)), key=lambda i: abs(times2Tr[i]-t0t))

	t0tb = 1.18e-09
	t0_b = min( range(len(times2Tr_bulk)), key=lambda i: abs(times2Tr_bulk[i]-t0tb))
	
	mtplot_cut = plt.subplot(325)
	mtplot_cut.plot(times2Tr[t0:len(times2Tr)-1], m2Tr[t0:len(times2Tr)-1],color="b")
	mtplot_cut.plot(times2Tr_bulk[t0_b:len(times2Tr_bulk)-1], m2Tr_bulk[t0_b:len(times2Tr_bulk)-1],color="r")
	mtplot_cut.set_title("m in selected range", fontsize=14)
	mtplot_cut.set_xlabel("time [s]")
	mtplot_cut.set_ylabel("m amp")

	try:
		print "2nd FFT bulk..."
		print (time.strftime("%I:%M:%S"))
		ts = timer()	
		mi_fitFFTc_bulk = np.fft.fft(m2Tr_bulk[t0_b:len(times2Tr_bulk)-1])
		freqc_bulk = np.fft.fftfreq(len(times2Tr_bulk[t0_b:len(times2Tr_bulk)-1]), dt)
		te = timer()
		print('CPU bulk: %.2fs' % (te - ts))

		print "2nd FFT..."
		print (time.strftime("%I:%M:%S"))
		ts = timer()	
		mi_fitFFTc = np.fft.fft(m2Tr[t0:len(times2Tr)-1])
		freqc = np.fft.fftfreq(len(times2Tr[t0:len(times2Tr)-1]), dt)
		te = timer()
		print('CPU: %.2fs' % (te - ts))
		

		mplot_cut = plt.subplot(326)
		mplot_cut.plot(freqc[w0:wf], np.abs(mi_fitFFTc[w0:wf]),color="b")
		mplot_cut.plot(freqc_bulk[w0:wf], np.abs(mi_fitFFTc_bulk[w0:wf]),color="r")
		mplot_cut.set_title("FFT of m in selected range", fontsize=14)
		mplot_cut.set_xlabel("omega [Hz]")
		mplot_cut.set_ylabel("m amp")
	except ValueError:
		print "Error: ", ValueError

	print "done."
	plt.show()
	fig = plt.gcf()
	plt.close()

if __name__ == "__main__":
	getData()