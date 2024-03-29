__author__ = 'TaytaInti'
# makes plots with results of simmulation using .dat files generated by oommf2matrix (MATLAB datas)
# important, show localisation of file /head.tcl/

import os
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.colors as colors

import struct

# NX  = 700
# X05 = 500
# Y05 = 200
# FI  = 75 * (np.pi/180)

def getData(filename):
    # print "getData"
    with open(filename, 'rb') as f:
        # print "omf file opened"
        headers = {} #I know valuemultiplier isn't always present. This is checked later.
        extraCaptures = {'SimTime':-1, 'Iteration':-1, 'Stage':-1, "MIFSource":""}
        #Parse headers
        a = ""
        # print "loading file"
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
        
        # print "loaded file, processing..."
        #Initialize array to be populated
        outArray = np.zeros((int(headers["xnodes"]),
                             int(headers["ynodes"]),
                             int(headers["znodes"]),
                             3))

        #Determine decoding mode and use that to populate the array
        # print "Data indicator:", a
        decode = a.split()
        if decode[3] == "Text":
            pass
            #return textDecode(f, outArray, headers, extraCaptures)
        elif (decode[3] == "Binary" or decode[3] == "binary")  and decode[4] == "4":
            #Determine endianness
            endianflag = f.read(4)
            if struct.unpack(">f", endianflag)[0] == 1234567.0:
                # print "Big-endian 4-byte detected."
                dc = struct.Struct(">f")
            elif struct.unpack("<f", endianflag)[0] == 1234567.0:
                # print "Little-endian 4-byte detected."
                dc = struct.Struct("<f")
            else:
                raise Exception("Can't decode 4-byte byte order mark: " + hex(endianflag))
            return _binaryDecode(f, 4, dc, outArray, headers, extraCaptures)
        elif decode[3] == "Binary" and decode[4] == "8":
            #Determine endianness
            endianflag = f.read(8)
            if struct.unpack(">d", endianflag)[0] == 123456789012345.0:
                # print "Big-endian 8-byte detected."
                dc = struct.Struct(">d")
            elif struct.unpack("<d", endianflag)[0] == 123456789012345.0:
                # print "Little-endian 8-byte detected."
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
    # print "Decode complete."
    return (targetarray, headers, extraCaptures)


def getCol(inArray, rowIndex, coord=2):
    nOfRows = len(inArray)
    nOfCols = len(inArray[0])
    # print " nOfRows=", nOfRows,"\n nOfCols=", nOfCols

    r=[]
    for row in rowIndex:
        t=[]
        for col in range(nOfCols):
            #for col in range(nOfCols):
            #print(inArray[0][row][col][0])
            a=(inArray[row][col][0])
            t.append( a[coord] )
        r.append(t)
    # print len(r), " , ", len(t)
    #print(t[100:120])
    return r


def processFiles(files, klisza_lok, dirLoc):
    nOfElements=20
    dane = np.zeros( ( int(len(klisza_lok)), nOfElements ))  # troche krytyczny moment

    # ftst = open("/home/pawel/2TB/mumax/mumax3.4_b3/waveguide_ft_v0.1.out/Ztest_klisza.txt", 'w')
    
    # xr=np.zeros(len(klisza_lok)) #Theoretical beam spot
    # for k in range(len(klisza_lok)):
    #     xr[k] = NX - (klisza_lok[k] - Y05 - (NX - X05)*np.tan(FI))/np.tan(FI)
    nf = 1
    nOfFiles = len(dirLoc)
    print "Number of files to process:, ", nOfFiles
    print "processing..."
    fileId = 0
    for filename in files: 
        fileId += 1
        print filename, fileId, "/", len(files)
        [matrix, headers, extraCaptures] = getData(filename)
        r=getCol(matrix, klisza_lok, 2) # getting slices
        # FINAL RESULT:
        #dane += map(lambda x: x*x, el )
        dane += [ [ x**2 for x in kk] for kk in r]
        for j in range(len(klisza_lok)):
            addr=filename[0: (len(filename)-4)] +"_SliceX_"+ str(klisza_lok[j])+".txt"
            f = open(addr, 'w')
            #print addr
            head=  "#SliceX " + str(klisza_lok[j]) +\
                "\n#SimTime " + str(extraCaptures['SimTime']) + \
                "\n#File " + str(filename) + \
                "\n#Points " + str(nOfElements) + \
                "\n#Data: \n"
            f.write(head)
            
            s = ""
            for i in range(len(r[j])):
                s = str( r[j][i] ) + "\n"
                f.write(s)
                s = ""
            #f.write("\n#End")
            f.close()
    print "done."
    #     ftst.write( str(r[0][15]**2) )
    #     ftst.write("\n")
    # ftst.close()

    
    #f.write("\nFINAL RESULT:\n")

    for j in range(len(klisza_lok)):
        addrFR=dirLoc+"final_results"+"_SliceX_"+ str(klisza_lok[j])+"FR.txt"
        fr = open(addrFR, 'w')
        fr.write(head)
        for i in range(len(r[j])):
            s = str( r[j][i] ) + "\n"
            fr.write(s)
        #f.write("\n#End")
        fr.close()
    
    
    # PLOT
    # x = np.arange(0., nOfElements, 1.0 )

    # colorsLi = ["b", "g", "r", "c", "m", "y", "b"]

    # ax = plt.subplot(111)
    # for i in range(len(klisza_lok)):
    #     #xr = NX - (klisza_lok[i] - Y05 - (NX - X05)*np.tan(FI))/np.tan(FI)
    #     plt.fill_between(x, 0, dane[i], color=colorsLi[i], label=str(klisza_lok[i]), alpha=0.3 )
    #     ax.annotate(str(klisza_lok[i]),
    #         xy=(xr[i], max(dane[i])), xycoords='data',
    #         xytext=(xr[i], 0), textcoords='data',
    #         size=15, va="center", ha="center",
    #         bbox=dict(boxstyle="round4", fc="w"),
    #         arrowprops=dict(arrowstyle="fancy",
    #                         fc=colorsLi[i], 
    #                         ec=colorsLi[i],
    #                         connectionstyle="arc3"), 
    #         color=colorsLi[i],
    #         )
        
    # plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    # #plt.plot(x, dane[1], 'g', label='y=-2')
    # plt.xlabel('x[*2nm]')
    # fig = plt.gcf()
    # plt.show() 
    # png_name = dirLoc+"results.png"
    # addr =  png_name
    # fig.savefig(addr, dpi=100)   
    # plt.close()

def findFiles(dir1, headTemp):
    filelist = []
    for (path, dirs, files) in os.walk(dir1):
        break
    for file in files:
        tail = file[ (len(file)-4) : (len(file))]
        head = file[0:len(headTemp)]
        if (tail == ".ovf" and head==headTemp):
            s = dir1+str(file)
            filelist.append(s)
    return filelist

if __name__ == "__main__":
    dirLoc = '/home/pawel/2TB/mumax/mumax3/waveguide_MC_v1.out/'
    filesList = findFiles(dirLoc, "m0")
    print "processed directory: ", dirLoc
    print "total number of processed files: ", len(filesList)
    print "\n\n"
    processFiles(filesList, [100, 250, 290, 900, 940], dirLoc)

    filesListB = findFiles(dirLoc, "B_ext")
    print "total number of processed files: ", len(filesListB)
    processFiles(filesListB, [100], dirLoc)




