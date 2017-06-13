#!/usr/bin/python
import subprocess as sp
import csv

#In a pixel array, 1 means solid dot, this method basic just return
#the length of the longest continuos dots
def longestLineLength(array):
    big = 0
    bigger = 0
    for i in array:
        if 1 == i:
            big = big + 1
        else:
            if big > bigger:
                bigger = big
            big = 0
    return bigger


#The 2D Cartesian coordinate system x,y is kind opposite to the 2D array in programming
#world, so instead introducing the concept of coordinate system, let's always use i, j
#always think in the row and column manner instead of mathmetical coordinate system
#this will return two array which can form up a mesh like thing
def getTableMeshIndex(binaryPic, tableBoundryThresh, fileWidth, fileHeight):
    #1st get two row index
    rowIndex = []
    for i in range(fileHeight):
        if longestLineLength(binaryPic[i,:]) > tableBoundryThresh:
            length = len(rowIndex)
            if 0 == length or i - rowIndex[length-1] > 1:
                rowIndex.append(i)
            else:
                rowIndex[length-1] = i
    #2nd get two col index
    colIndex = []
    for j in range(fileWidth):
        if longestLineLength(binaryPic[:,j]) > tableBoundryThresh:
            length = len(colIndex)
            if 0 == length or j - colIndex[length-1] > 1:
                colIndex.append(j)
            else:
                colIndex[length-1] = j

    assert(len(rowIndex) >= 2)
    assert(len(colIndex) >= 2)
    return {"rowIndex":rowIndex, "colIndex":colIndex}

#pdftotext uses Cartesian coordiante, so need to be very careful here
def getCellText(fileName, pageNum, upRowIndex, cellHeight, leftColIndex, cellWidth, ppi):
    cmd=("pdftotext -r {0} -x {1} -y {2} -W {3} -H {4} -layout -nopgbrk -f {5} -l {6} {7} -"\
            ).format(ppi, leftColIndex, upRowIndex, cellWidth, cellHeight,
            pageNum, pageNum, fileName)
    p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, shell=True)
    txt = p.communicate()[0]
    txt = txt.replace('\xe2', '-')
    txt = txt.replace('\xc2', '')
    txt = txt.replace('\x80', '')
    txt = txt.replace('\x93', '')
    return " " + txt.strip() #Excel treats 8-3 as 8-MAR, just pre-append space


def createCSV(filePath, dataRows):
    with open(filePath, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(dataRows)

def printUsage():
    print """Usage: bbpy tableFromPdf.py [options] -i <input pdf file>
    OPIONS:
    -r : converting resolution, default to 300, which seems to be ideal
    -f : starting page number in pdf to convert default to 1
    -l : ending page number in pdf to convert default to 1
    -o : output csv file, default to out.csv
    -tbt : table boundry pixel length threshold, anything large will be treated as an edge,
           default to 500 pixel, which seems good (Need to have a better calculation here)
    -h | --help : print usage"""
    