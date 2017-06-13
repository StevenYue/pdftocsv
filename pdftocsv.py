#!/usr/bin/python
import subprocess as sp
from numpy import fromstring, uint8, reshape, where, ones, sum, zeros, diff
import operator
import sys
import util as ut
import re

g_ppi = 300
g_tableBoundryThresh = 500
g_csvMatrix = []
g_firstPage = 1
g_lastPage = 1
g_fileName = ""
g_outFile = "out.csv"

#check commandline override
if len(sys.argv) < 2:
    ut.printUsage()
    sys.exit()
args = sys.argv[1:]
i = 0
while i < len(args):
    if "-r" == args[i]:
        i = i + 1
        g_ppi = int(args[i])
    elif "-f" == args[i]:
        i = i + 1
        g_firstPage = int(args[i])
    elif "-l" == args[i]:
        i = i + 1
        g_lastPage = int(args[i])
    elif "-tbt" == args[i]:
        i = i + 1
        g_tableBoundryThresh = int(args[i])
    elif "-i" == args[i]:
        i = i + 1
        g_fileName = args[i]
    elif "-o" == args[i]:
        i = i + 1
        g_outFile = args[i]
    elif "-h" == args[i] or "--help" == args[i]:
        ut.printUsage()
        sys.exit()
    i = i + 1
if "" == g_fileName:
    ut.printUsage()
    sys.exit()

p = g_firstPage
while p <= g_lastPage:
    cmd=("pdftoppm -gray -r {0} -f {1} -l {2} {3}").format(g_ppi, p, p, g_fileName)
    out = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, shell=True)

    fd = out.stdout

    fd.readline() #1st line is useless
    one, two = fd.readline().split()
    maxVal = int(fd.readline())
    fileWidth=int(one)
    fileHeight=int(two)

    unreadableData = fd.read()

    data = fromstring(unreadableData, dtype=uint8)
    data = reshape(data, (fileHeight, fileWidth))

    binaryPic = ones((fileHeight, fileWidth), dtype=int)
    binaryPic[0:fileHeight, 0:fileWidth] = (data[:,:] != 255) #White:0, None-white:1

    #1st find the boundaries of the table
    meshIndex = ut.getTableMeshIndex(binaryPic, g_tableBoundryThresh, fileWidth, fileHeight)

    #2nd with this mesh, we can try to extract the data
    meshWidth = len(meshIndex["colIndex"])
    meshHeight = len(meshIndex["rowIndex"])

    for i in range(meshHeight-1):
        row = []
        for j in range(meshWidth-1):
            upRow = meshIndex["rowIndex"][i]
            cellHeight = meshIndex["rowIndex"][i+1] - upRow
            leftCol = meshIndex["colIndex"][j]
            cellWidth = meshIndex["colIndex"][j+1] - leftCol
            txt =ut.getCellText(g_fileName, p, upRow, cellHeight, leftCol, cellWidth, g_ppi)
            row.append(txt)
        g_csvMatrix.append(row)
    p = p + 1
ut.createCSV(g_outFile, g_csvMatrix)
