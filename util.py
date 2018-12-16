import math
import copy
def normalize(data):
    pass
def readData(path):
    dictL2I = {}
    dictI2L = {}
    NClass = 0
    file=open(path)
    data = []
    for x in file.readlines():
        d = []
     #   print(x.split(','))
        l = x.split(',')
        #print(l)
        for i in l[:-1]:
            d.append(float(i))
        str = l[len(l)-1][:-1]
        #print("str:",str)
        if (str not in dictL2I.keys() and str != ''):
            NClass += 1
            dictL2I[str] = NClass
            dictI2L[NClass] = str
        if(str != ''):
            d.append(dictL2I[str])
            data.append(d)

    #print(dictL2I)
    #print(data)
    data = data[:-1]
    maxVal = copy.deepcopy(data[0][:-1])
    minVal = copy.deepcopy(data[0][:-1])
    for d in data:
        for i in range(len(maxVal)):
            if(maxVal[i]<d[i]):
                maxVal[i] = d[i]
            if(minVal[i]>d[i]):
                minVal[i] = d[i]
    dRange = []
    #print(minVal,maxVal)
    for i in range(len(maxVal)):
        dRange.append(maxVal[i]-minVal[i])
    #print(dRange)
    for d in data:
        for i in range(len(d)-1):
            d[i] = (d[i]-minVal[i])/dRange[i]

    #for d in data:
     #   print(d)
    return data,NClass,dictL2I,dictI2L



# path = "./data/iris.dat"
# readData(path)