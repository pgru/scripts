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
	# strs = "foo\tbar\t\tspam"
	# print re.split(r'\t+', strs)

	
	print filename
	# t0t = 10e-09
	# tkt = 30e-09
	a = ""
	with open(filename, 'rb') as f:
		# t
		print f.readline()
		# while not "#Data:" in a:
		# 	a = f.readline().strip()

		i=0
		print "reading file..."
		times2Tr = []
		m2Tr_z = []
		m2Tr_x = []
		m2Tr_y = []
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
	# print len(freq), max(freq), min(freq)

	
	# print t0, type(t0), len(times2Tr)
	# print times2Tr[t0]

	# d =  [] #cuda.to_device( cufftComplex, stream=stream1 )
	# ts = timer()
	# yi_fitFFT = cufft.fft(amp2Tr, out=d)
	# yi_fit_freq = cufft.fftfreq(len(times2Tr), dt)
	# te = timer()
	# print('GPU: %.2fs' % (te - ts))


	# btplot = plt.subplot(321)
	# btplot.plot(times2Tr[0:tk], b2Tr[0:tk],color="g", label=r'$B_{x}$')
	# # btplot.set_title(r'$B_{ext}$', fontsize=14)
	# btplot.set_xlabel("time [s]")
	# btplot.set_ylabel(r'$B_{ext}$ [T]')
	# btplot.legend(ncol=1, fancybox=True, shadow=True)

	# bplot = plt.subplot(322)
	# bplot.plot(freq[w0:wf], np.abs(bi_fitFFT[w0:wf]),color="g", label=r'$B_{x}$')
	# bplot.set_title("FFT", fontsize=16)
	# # bplot.set_xlabel(r'$\nu$ [Hz]')
	# # bplot.set_ylabel(r'$B_{ext}$', fontsize=16)
	# bplot.legend(ncol=1, fancybox=True, shadow=True)

	# mtplot = plt.subplot(323)
	# mtplot.plot(times2Tr[0:tk], m2Tr_z[0:tk],color="b", label=r'$m_{z}$')
	# mtplot.plot(times2Tr[0:tk], m2Tr_x[0:tk],color="r", label=r'$m_{x}$')
	# mtplot.plot(times2Tr[0:tk], m2Tr_y[0:tk],color="g", label=r'$m_{y}$')
	# # mtplot.set_title("m", fontsize=14)
	# mtplot.set_xlabel("time [s]")
	# mtplot.set_ylabel(r'$m$', fontsize=16)
	# mtplot.legend(ncol=1, fancybox=True, shadow=True)

	# mplot = plt.subplot(324)
	# mplot.plot(freq[w0:wf], np.abs(mi_fitFFT_z[w0:wf]),color="b", label=r'$m_{z}$')
	# mplot.plot(freq[w0:wf], np.abs(mi_fitFFT_x[w0:wf]),color="r", label=r'$m_{x}$')
	# mplot.plot(freq[w0:wf], np.abs(mi_fitFFT_y[w0:wf]),color="g", label=r'$m_{y}$')
	# # mplot.set_title("FFT of m", fontsize=14)
	# # mplot.set_xlabel(r'$\nu$ [Hz]')
	# # mplot.set_ylabel(r'$m$', fontsize=16)
	# mplot.legend(ncol=1, fancybox=True, shadow=True)

	
	# mtplot_cut = plt.subplot(325)
	# mtplot_cut.plot(times2Tr[t0:tk], m2Tr_z[t0:tk],color="b", label=r'$m_{z}$')
	# mtplot_cut.plot(times2Tr[t0:tk], m2Tr_x[t0:tk],color="r", label=r'$m_{x}$')
	# # mtplot_cut.plot(times2Tr[t0:tk], m2Tr_y[t0:tk],color="g", label=r'$m_{y}$')
	# # mtplot_cut.set_title("m in selected range", fontsize=14)
	# mtplot_cut.set_xlabel("time [s]")
	# mtplot_cut.set_ylabel(r'$m$', fontsize=16)
	# mtplot_cut.legend(ncol=1, fancybox=True, shadow=True)
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
		

		# mplot_cut = plt.subplot(326)
		# mplot_cut.plot(freqc[w0:wf], np.abs(mi_fitFFT_zc[w0:wf]),color="b", label=r'$m_{z}$')
		# mplot_cut.plot(freqc[w0:wf], np.abs(mi_fitFFT_xc[w0:wf]),color="r", label=r'$m_{x}$')
		# # mplot_cut.plot(freqc[w0:wf], np.abs(mi_fitFFT_yc[w0:wf]),color="g", label=r'$m_{y}$')
		# # mplot_cut.set_title("FFT of m in selected range", fontsize=14)
		# mplot_cut.set_xlabel(r'$\nu$ [Hz]')
		# # mplot_cut.set_ylabel(r'$m$', fontsize=16)
		# mplot_cut.legend(ncol=1, fancybox=True, shadow=True)
		# print "max freq: ", max(freqc)

	except ValueError:
		print "Error: ", ValueError

	print "done."
	# mplot_cut.legend(ncol=1, fancybox=True, shadow=True)
	# plt.show()
	# fig = plt.gcf()
	# plt.close()
	return [freqc[w0:wf], np.abs(mi_fitFFT_xc[w0:wf]), np.abs(mi_fitFFT_yc[w0:wf]), np.abs(mi_fitFFT_zc[w0:wf])]

# filename = 'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\200nm\\200nm_Ha_0.3_r_8.5.out\\table.txt'
	# filename = 'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\300nm\\300nm_Ha_0.3_r_8.5.out\\table.txt'
	# filename = 'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\400nm\\400nm_Ha_0.3_r_8.5.out\\table.txt'
	# filename = 'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\500nm\\500nm_Ha_0.3_r_8.5.out\\table.txt'
	# filename = 'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\200nm\\200nm_Ha_0.3_r_7.out\\table.txt'
	# filename = 'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\300nm\\300nm_Ha_0.3_r_7.out\\table.txt'
	# filename = 'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\400nm\\400nm_Ha_0.3_r_7.0.out\\table.txt'
	# filename = 'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\500nm\\500nm_Ha_0.3_r_7.out\\table.txt'

	# filename = 'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\200nm\\200nm_Ha_0.3_r_9.0.out\\table.txt'
	# filename = 'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\300nm\\300nm_Ha_0.3_r_9.0.out\\table.txt'
	# filename = 'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\400nm\\400nm_Ha_0.3_r_9.0.out\\table.txt'
	# filename = 'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\500nm\\500nm_Ha_0.3_r_9.out\\table.txt'

	# filename = 'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\200nm\\200nm_Ha_0.3_r_11.out\\table.txt'
	# filename = 'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\300nm\\300nm_Ha_0.3_r_11.out\\table.txt'
	# filename = 'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\400nm\\400nm_Ha_0.3_r_11.0.out\\table.txt'
	# filename = 'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\500nm\\500nm_Ha_0.3_r_11.out\\table.txt'

	# filename = 'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\200nm\\200nm_Ha_0.3_r_10.out\\table.txt'
	# filename = 'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\200nm\\200nm_Ha_0.3_r_12.5.out\\table.txt'
	# filename = 'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\200nm\\deep_200nm_Ha_0.3_r_8.5.out\\table.txt'
	# filename = 'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\500nm\\500nm_Ha_0.3_r_12.5.out\\table.txt'
	# filename = 'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\500nm\\deep_500nm_Ha_0.3_r_8.5.out\\table.txt'
	# filename = 'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\300nm\\deep_300nm_Ha_0.3_r_8.5.out\\table.txt'
	# filename = 'C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\400nm\\deep_400nm_Ha_0.3_r_8.5.out\\table.txt'
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
		
	
	[f, mx, my, mz] = getData(li_9nm[0], w0t, wft, t0t, tkt)
	p200 = plt.subplot(411)
	p200.fill_between(f, 0, mx,color="b", label=r'$m_{x}$', alpha=0.5)
	p200.fill_between(f, 0, mz,color="r", label=r'$m_{z}$', alpha=0.5)
	p200.set_ylabel(r'$a=200nm$', fontsize=16)
	p200.set_xlabel(r'$\nu$ [Hz]')
	# mplot_cut.set_ylabel(r'$m$', fontsize=16)
	p200.legend(ncol=1, fancybox=True, shadow=True)
	print "2nd file..."
	# mplot_cut.plot(freqc[w0:wf], np.abs(mi_fitFFT_zc[w0:wf]),color="b", label=r'$m_{z}$')
	[f, mx, my, mz] = getData(li_9nm[1], w0t, wft, t0t, tkt)
	p300 = plt.subplot(412)
	p300.fill_between(f, 0, mx,color="b", label=r'$m_{x}$', alpha=0.5)
	p300.fill_between(f, 0, mz,color="r", label=r'$m_{z}$', alpha=0.5)
	p300.set_ylabel(r'$a=300nm$', fontsize=16)
	p300.set_xlabel(r'$\nu$ [Hz]')
	# p300.set_ylabel(r'$m$', fontsize=16)
	p300.legend(ncol=1, fancybox=True, shadow=True)
	[f, mx, my, mz] = getData(li_9nm[2], w0t, wft, t0t, tkt)
	p400 = plt.subplot(413)
	p400.fill_between(f, 0, mx,color="b", label=r'$m_{x}$', alpha=0.5)
	p400.fill_between(f, 0, mz,color="r", label=r'$m_{z}$', alpha=0.5)
	p400.set_ylabel(r'$a=400nm$', fontsize=16)
	p400.set_xlabel(r'$\nu$ [Hz]')
	# p400.set_ylabel(r'$m$', fontsize=16)
	p400.legend(ncol=1, fancybox=True, shadow=True)
	[f, mx, my, mz] = getData(li_9nm[3], w0t, wft, t0t, tkt)
	p500 = plt.subplot(414)
	p500.fill_between(f, 0, mx,color="b", label=r'$m_{x}$', alpha=0.5)
	p500.fill_between(f, 0, mz,color="r", label=r'$m_{z}$', alpha=0.5)
	p500.set_ylabel(r'$a=500nm$', fontsize=16)
	p500.set_xlabel(r'$\nu$ [Hz]')
	# p500.set_ylabel(r'$m$', fontsize=16)
	p500.legend(ncol=1, fancybox=True, shadow=True)

	plt.suptitle(r'$dr=9nm$', fontsize=20)
	plt.show()
	fig = plt.gcf()
	plt.close()