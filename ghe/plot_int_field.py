bbbb__author__ = 'TaytaInti'
# makes plots with results of simmulation using .dat files generated by oommf2matrix (MATLAB datas)
# important, show localisation of file /head.tcl/

import os
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.colors as colors

import re as re
import struct


def getData(filename):
    print "getData" 
    with open(filename, 'rb') as f:
        print "omf file opened"
        headers = {} #I know valuemultiplier isn't always present. This is checked later.
        extraCaptures = {'SimTime':-1, 'Iteration':-1, 'Stage':-1, "MIFSource":""}
        #Parse headers
        a = ""
        print "loading file"
        while not "Begin: Data" in a:
            a = f.readline().strip()
            #Determine if it's actually something we need as header data
            for key in ["xbase", "ybase", "zbase", "xstepsize", "ystepsize", "zstepsize", "xnodes", "ynodes", "znodes", "valuemultiplier"]:
                if key in a:
                    headers[key] = float(a.split()[2]) #Known position FTW
            #All right, it may also be time data, which we should capture
            if "Total simulation time" in a:
                #Split on the colon to get the time with units; strip spaces and split on the space to separate time and units
                #Finally, pluck out the time, stripping defensively (which should be unnecessary).
                extraCaptures['SimTime'] = float(a.split(":")[-1].strip().split()[0].strip())
            if "Iteration:" in a:
                #Another tricky split...
                extraCaptures['Iteration'] = float(a.split(":")[2].split(",")[0].strip())
            if "Stage:" in a:
                extraCaptures['Stage'] = float(a.split(":")[2].split(",")[0].strip())
            if "MIF source file" in a:
                extraCaptures['MIFSource'] = a.split(":",2)[2].strip()
        
        print "loaded file, processing..."
        #Initialize array to be populated
        outArray = np.zeros((int(headers["xnodes"]),
                             int(headers["ynodes"]),
                             int(headers["znodes"]),
                             3))

        #Determine decoding mode and use that to populate the array
        print "Data indicator:", a
        decode = a.split()
        if decode[3] == "Text":
            pass
            #return textDecode(f, outArray, headers, extraCaptures)
        elif (decode[3] == "Binary" or decode[3] == "binary")  and decode[4] == "4":
            #Determine endianness
            endianflag = f.read(4)
            if struct.unpack(">f", endianflag)[0] == 1234567.0:
                print "Big-endian 4-byte detected."
                dc = struct.Struct(">f")
            elif struct.unpack("<f", endianflag)[0] == 1234567.0:
                print "Little-endian 4-byte detected."
                dc = struct.Struct("<f")
            else:
                raise Exception("Can't decode 4-byte byte order mark: " + hex(endianflag))
            return _binaryDecode(f, 4, dc, outArray, headers, extraCaptures)
        elif decode[3] == "Binary" and decode[4] == "8":
            #Determine endianness
            endianflag = f.read(8)
            if struct.unpack(">d", endianflag)[0] == 123456789012345.0:
                print "Big-endian 8-byte detected."
                dc = struct.Struct(">d")
            elif struct.unpack("<d", endianflag)[0] == 123456789012345.0:
                print "Little-endian 8-byte detected."
                dc = struct.Struct("<d")
            else:
                raise Exception("Can't decode 8-byte byte order mark: " + hex(endianflag))
            return _binaryDecode(f, 8, dc, outArray, headers, extraCaptures)
        else:
            raise Exception("Unknown OOMMF data format:" + decode[3] + " " + decode[4])

def _binaryDecode(filehandle, chunksize, decoder, targetarray, headers, extraCaptures):
    valm = headers.get("valuemultiplier",1)
    for k in range(int(headers["znodes"])):
        for j in range(int(headers["ynodes"])):
            for i in range(int(headers["xnodes"])):
                for coord in range(3): #Slowly populate, coordinate by coordinate
                    targetarray[i,j,k,coord] = decoder.unpack(filehandle.read(chunksize))[0] * valm
    print "Decode complete."
    return (targetarray, headers, extraCaptures)


def dirArray(inArray, dir):
    if   dir == 'x':  d = 0
    elif dir == 'y':  d = 1
    elif dir == 'z':  d = 2
    outArray = []
    for row in inArray:
        t = []
        for col in row:
            t.append(col[0][d])
            #print col[0][dir]
        outArray.append(t)
    return outArray

def cut_extr(x, max = 2000):
            xm = np.sqrt(x**2)
            if xm > max: return max * (x/xm)
            else: return x

# filtrowanie, usuwanie marginesow i za duzych wartosci
def filter_map(x, padding = 50, max = np.Inf):
        f = []
        for item in [item for item in x 
                     if ( (x.index(item) > padding) and x.index(item) < (len(x)- padding) )]:
            f.append( [elem for elem in item if (item.index(elem) > padding and (item.index(elem) < (len(item) - padding)) ) ])
        
        result = []
        for item in f:
            result.append( map(cut_extr, item) )  
        return result    

class FilterMap(object):
    u"filtrowanie mapy, zmiana maximum, wycinanie marginesow wzdluz Y"
    def __init__(self, max_val = np.Inf , padding = 0):
        self.max = max_val
        self.padding = padding
    def filter(self, map1):
        f = []
        for r in range(len(map1)):
            f0 = []
            for c in range(len(map1[0]) - 2*self.padding):
                cell = map1[r][c+self.padding]
                if np.sqrt(cell**2) < self.max:
                    f0.append( cell )
                else: f0.append(self.max*np.sqrt(cell**2)/cell)
            f.append(f0)
        self.result = f

def pproc(filename, inArray, dir, max_value, padding, show_plot):
    array = dirArray(inArray[0], dir)
    #with open('1.dat', 'w') as f:
    #    for item in xArray:    
    #        f.write(str(item))
    mat = FilterMap(max_value, padding)
    mat.filter(array)
    #plt.imshow(mat.result)
    
    maxV =  max(map(max, mat.result))
    minV =  min(map(min, mat.result))
    if (maxV**2 > minV**2): mv = np.sqrt(maxV**2)
    else: mv = np.sqrt(minV**2)

    print "max value of field: ", mv
    print "half of max value of field: ", mv/2
    
    # ['Spectral', 'summer', 'RdBu', 'Set1', 'Set2', 'Set3', 'brg_r', 'Dark2', 
    # 'hot', 'PuOr_r', 'afmhot_r', 'terrain_r', 'PuBuGn_r', 'RdPu', 'gist_ncar_r', 
    # 'gist_yarg_r', 'Dark2_r', 'YlGnBu', 'RdYlBu', 'hot_r', 'gist_rainbow_r', 
    # 'gist_stern', 'gnuplot_r', 'cool_r', 'cool', 'gray', 'copper_r', 'Greens_r', 
    # 'GnBu', 'gist_ncar', 'spring_r', 'gist_rainbow', 'RdYlBu_r', 'gist_heat_r', 
    # 'OrRd_r', 'bone', 'gist_stern_r', 'RdYlGn', 'Pastel2_r', 'spring', 'terrain', 
    # 'YlOrRd_r', 'Set2_r', 'winter_r', 'PuBu', 'RdGy_r', 'spectral', 'flag_r', 
    # 'jet_r', 'RdPu_r', 'Purples_r', 'gist_yarg', 'BuGn', 'Paired_r', 'hsv_r', 'bwr', 
    # 'YlOrRd', 'Greens', 'PRGn', 'gist_heat', 'spectral_r', 'Paired', 'hsv', 'Oranges_r', 
    # 'prism_r', 'Pastel2', 'Pastel1_r', 'Pastel1', 'gray_r', 'PuRd_r', 'Spectral_r', 
    # 'gnuplot2_r', 'BuPu', 'YlGnBu_r', 'copper', 'gist_earth_r', 'Set3_r', 'OrRd', 
    # 'PuBu_r', 'ocean_r', 'brg', 'gnuplot2', 'jet', 'bone_r', 'gist_earth', 'Oranges', 
    # 'RdYlGn_r', 'PiYG', 'YlGn', 'binary_r', 'gist_gray_r', 'Accent', 'BuPu_r', 'gist_gray', 
    # 'flag', 'seismic_r', 'RdBu_r', 'BrBG', 'Reds', 'BuGn_r', 'summer_r', 'GnBu_r', 'BrBG_r', 
    # 'Reds_r', 'RdGy', 'PuRd', 'Accent_r', 'Blues', 'Greys', 'autumn', 'PRGn_r', 'Greys_r', 
    # 'pink', 'binary', 'winter', 'gnuplot', 'pink_r', 'prism', 'YlOrBr', 'rainbow_r', 'rainbow', 
    # 'PiYG_r', 'YlGn_r', 'Blues_r', 'YlOrBr_r', 'seismic', 'Purples', 'bwr_r', 'autumn_r', 
    # 'ocean', 'Set1_r', 'PuOr', 'PuBuGn', 'afmhot']
    # norm = colors.normalize(-mv, mv)
    # MUMAX
    norm = colors.normalize(-1, 1)
    # norm = colors.LogNorm()
    # plt.matshow(mat.result, cmap='RdBu', norm=colors.LogNorm() )
    plt.matshow(mat.result, norm=norm )
    plt.colorbar(shrink=.8)
    fig = plt.gcf()
    if (show_plot==True): plt.show()
    png_name = filename[0:(len(filename)-4)] + "_" "+.png"
    a = re.split(r'\\', png_name)
    addr = ""
    for i in range(len(a)-1):
        addr += a[i] +"\\"
    print addr
    addr += (dir+"_"+a[ len(a)-1 ])
    print addr
    #addr =  nn
    fig.savefig(addr, dpi=100)
    plt.close()


# wybieranie kierunku w ktorym liczy?
def processFile(filename, mdir='x', cdir = 'x'):
    inArray= getData(filename)
    array = dirArray(inArray[0], mdir)
    print len(array), len(array[0])
    data_y = array[ int(len(array)/2)]
    data_x = [ x[int(len(array)/2)] for x in array ]
    y= [2*x for x in range(len(array[int(len(array)/2)]))]
    x= [2*x for x in range(len(array))]
    if cdir== 'x': return [x, data_x]
    elif cdir== 'y': return [y, data_y]

def pFiles(path):
    for (path, dirs, files) in os.walk(path):
        break
    for file in files:
        tail = file[ (len(file)-4) : (len(file))]
        if tail ==  ".ovf":
            print file
    for file in files:
        tail = file[ (len(file)-4) : (len(file))]
        #head= file[0:6]
        if (tail == ".ovf"):
            print "next file: ", file
            addr = path + str(file)
            print file
            processFile(addr, True, True, True, False)
            print "waiting for next file"
    print "end of the loop"

if __name__ == "__main__":
    # processFile('C:\\Users\\Pawel\\workspace\\mumax3\\barman_semanti\\04.05\\500nm\\500nm_Ha_0.3_r_8.5.out\\m_stab.ovf', 'x', True)
    [x_Co, y_Co] = processFile(filename='C:\\Users\\Pawel\\workspace\\ghe_pcss\\static_conf\\Co_45.out\\B_eff.ovf',  mdir='x', cdir='x')
    [x_yig, y_yig] = processFile(filename='C:\\Users\\Pawel\\workspace\\ghe_pcss\\static_conf\\yig_45.out\\B_eff.ovf',  mdir='x', cdir='x')
    [x_py, y_py] = processFile(filename='C:\\Users\\Pawel\\workspace\\ghe_pcss\\static_conf\\py_45.out\\B_eff.ovf',  mdir='x', cdir='x')
    
    plt.plot(x_Co, y_Co, color='r', lw=2, label='Co')
    plt.plot(x_yig, y_yig, color='b', lw=2, label='YIG')
    plt.plot(x_py, y_py, color='g', lw=2, label='Py')
    plt.fill_between(x_Co, y_Co,  y_yig, color='k', alpha=0.1, hatch="//")
    plt.xlabel('[nm]', size='large')
    plt.ylabel(r'$B$ [T]', size='large')
    plt.title(r'$B_{eff}$', size='x-large')
    plt.legend(ncol=1, fancybox=True, shadow=True, loc="lower center")
    plt.show()
    plt.close() 