__author__ = 'TaytaInti'
# process all files in directory

import os
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from string import digits

import struct


def getData(filesList, showPlot=True, nx=1300):
    # print "getData"
    data = np.zeros(nx)
    idx = 0
    for filename in filesList: 
        with open(filename, 'rb') as f:
            # print filename
            #print "file opened"
            headers = {} #I know valuemultiplier isn't always present. This is checked later.
            #Parse headers
            a = ""
            #print "loading file"
            while not "#Data:" in a:
                a = f.readline().strip()
                #Determine if it's actually something we need as header data
                for key in ["SliceX", "BeamSpot", "SimTime", "File","Points"]:
                    if key in a:
                        headers[key] = str(a.split()[1]) #Known position FTW
            res = []
            while True:
                a = f.readline().strip()
                if len(a)==0:
                    break # EOF
                res.append(float(a))
            #print len(res)
            data += map(lambda x: x*x, res )

            idx += 1
            #data += res
    # print idx
    # print "max: ", max(data)
    maxId = data.tolist().index(max(data))
    # print maxId
    leftLi = data[0:(maxId-1)].tolist()
    rightLi= data[(maxId+1):(len(data)-1)]
    
    left05 = min(range(len(leftLi)), key=lambda i: abs(leftLi[i]-max(data)/2))
    right05= min(range(len(rightLi)), key=lambda i: abs(rightLi[i]-max(data)/2))
    right05_loc = right05 + len(leftLi)+2
    
    centerV = 0.5*(right05_loc+left05)
    # print "max: ", max(data)/2
    # print right05_loc, len(data)
    # print left05, leftLi[left05]
    # print right05,rightLi[right05]
    # print "centerV: ", centerV
            
    #data = map(lambda x: x*x, data )

    x = np.arange(0., len(data), 1.0 )
    colorsLi = ["r", "g", "b", "c", "m", "y", "b"]
    ax = plt.subplot(111)
    #xr = nx - (klisza_lok[i] - Y05 - (nx - X05)*np.tan(FI))/np.tan(FI)
    plt.fill_between(x, 0, data, color=colorsLi[2], label=headers["SliceX"], alpha=0.5)
    plt.plot( [0, nx-1], [max(data)/2, max(data)/2], color=colorsLi[2])
    
    ax.annotate(str(left05),
        xy=(left05, leftLi[left05]), xycoords='data',
        xytext=(left05, 0), textcoords='data',
        size=15, va="center", ha="center",
        bbox=dict(boxstyle="round4", fc="w"),
        arrowprops=dict(arrowstyle="fancy",
                        fc=colorsLi[2], 
                        ec=colorsLi[2],
                        connectionstyle="arc3"), 
        color=colorsLi[2],
        )
    ax.annotate(str(right05_loc),
        xy=(right05_loc, rightLi[right05]), xycoords='data',
        xytext=(right05_loc, 0), textcoords='data',
        size=15, va="center", ha="center",
        bbox=dict(boxstyle="round4", fc="w"),
        arrowprops=dict(arrowstyle="fancy",
                        fc=colorsLi[2], 
                        ec=colorsLi[2],
                        connectionstyle="arc3"), 
        color=colorsLi[2],
        )
    ax.annotate(str(centerV),
        xy=(centerV, max(data)), xycoords='data',
        xytext=(centerV, 0), textcoords='data',
        size=15, va="center", ha="center",
        bbox=dict(boxstyle="round4", fc="w"),
        arrowprops=dict(arrowstyle="fancy",
                        fc=colorsLi[0], 
                        ec=colorsLi[0],
                        connectionstyle="arc3"), 
        color=colorsLi[0],
        )

    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    #plt.plot(x, dane[1], 'g', label='y=-2')
    plt.xlabel('x[*2nm]')
    plt.ylabel('Amp')
    plt.suptitle('Film', fontsize=20)
    fig = plt.gcf()
    if showPlot==True: plt.show() 
    png_name = filename[0: (len(filename)-4)] + ".png"
    addr =  png_name
    fig.savefig(addr, dpi=100)   
    plt.close()
    # zwrot wartosci piku
    xTxt = filename[(len(filename)-8): (len(filename)-4)]
    # xCoord= int(xTxt.replace("_", ""))
    xCoord = ''.join(c for c in xTxt if c in digits)
    return [int(xCoord), centerV]

def findFiles1(dir1):
    filelist = []
    for (path, dirs, files) in os.walk(dir1):
        break
    for file in files:
        tail = file[ (len(file)-8) : (len(file))]
        #head= file[0:6]
        if (tail == "X_90.txt"):
            s = dir1+str(file)
            filelist.append(s)
    return filelist

def findFiles(dir1, minV, maxV):
    filelist = []
    coords = []
    for (path, dirs, files) in os.walk(dir1):
        break
    for file in files:
        tail = file[ (len(file)-8) : (len(file))]
        #print tail[(len(tail)-4):len(tail)] # tail[(len(file)-8):(len(file))]
        head= file[0:2]
        try:
            tailN = int(''.join(c for c in tail if c in digits))
            if ( tail[(len(tail)-4):len(tail)]==".txt" \
                    and head == "m0" \
                    and tailN > minV and tailN <= maxV ): 
                s = dir1+str(file)
                filelist.append(s)
                try: coords.index(tailN)
                except: coords.append(tailN)
        except ValueError:
            print "Error in processing file:", file
    return filelist, sorted(coords)

def process(filesList, coords, fname, nx1):
    f = open(fname, 'w')
    for coord in coords:
        files = []
        for fileN in filesList:
            tail = fileN[ (len(fileN)-8) : (len(fileN))]
            tailN = int(''.join(c for c in tail if c in digits))
            if tailN==coord:
                files.append(fileN)
        files = sorted(files)
        # print files
        r = getData(files, showPlot=False, nx=nx1)
        print r[0], r[1]
        s = ""
        for item in r: s+= str(item)+"\t"
        s += "\n"
        f.write(s)
        #f.write("\n#End")
    f.close()
if __name__ == "__main__":
    dirLoc = "/home/pawel/2TB/mumax/mumax3/ghe_60.2process/"
    cut=700
    N=900
    [filesInc, coordsInc] = findFiles(dirLoc, 0, cut)
    print coordsInc
    fname = dirLoc+"__res_max_inc.txt"
    process(filesInc, coordsInc, fname, nx1=N)

    [filesRefl, coordsRefl] = findFiles(dirLoc, cut, np.Inf)
    print coordsRefl
    fname = dirLoc+"__res_max_refl.txt"
    process(filesRefl, coordsRefl, fname, nx1=N)

    #print filesList
   