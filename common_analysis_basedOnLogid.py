# -*- coding: utf-8 -*-
import os
import sys
import time
import string

#  This program is userd for analysis log file baseed on UUID, if you would like to use this program, please follow the following rules:
#       1. please diviide the log with characteristic ';', first contains method name and code block position, second is UUID, third is costed time between start and current position
#       2. we need you input request start flag, request end flag, and a string divided by characteristic ';' as different position
#       3. if the program exit before request end flag, we assume there contain some error, please analysis it later, and this record will not be compute
#       4. request end flag can be the same one of the last on in position list


#return string(error reason)
def isExistingStop(dict_partitionalTime,partitionalNames, logId):
    partitionalNameList = partitionalNames.split(";")
    for partitionalName in partitionalNameList:
        if dict_partitionalTime.has_key(partitionalName) == False:
            return "unknownErrorReason"
        if dict_partitionalTime[partitionalName].has_key(logId) == False:
            return partitionalName+"Stoped"
    return "noStop"

#return dict(log info dict)
def readLogfile(filename, partitionalNames, requestStartFlag, requestEndFlag):
    dict_totalTime = dict()
    dict_methodName = dict()
    dict_partitionalTime = dict()
    partitionalNameList = partitionalNames.split(";")
    for partitionalName in partitionalNameList:
        dict_partitionalTime[partitionalName] = dict()
    file_source = open(filename, "r")
    for line in file_source.readlines():
        valueList = line.split(";")
        costTime = valueList[2]
        if requestStartFlag in valueList[0]:
            methodList = valueList[0].split(" ")
            methodName = methodList[len(methodList)-2]
            dict_methodName[valueList[1]] = methodName
        elif costTime.isdigit() and dict_methodName.has_key(valueList[1]):
            time = string.atoi(valueList[2]) 
            for partitionalName in partitionalNameList:
                if partitionalName in valueList[0]:
                    dict_partitionalTime[partitionalName][valueList[1]] = time
            if dict_totalTime.has_key(valueList[1]) == False:
                dict_totalTime[valueList[1]] = time
            elif dict_totalTime[valueList[1]] < time:
                dict_totalTime[valueList[1]] = time
    file_source.close()
    dict_result = dict()
    dict_result["dict_totalTime"] = dict_totalTime
    dict_result["dict_methodName"] = dict_methodName
    dict_result["dict_partitionalTime"] = dict_partitionalTime
    return dict_result
                

#return dict(dict_errorReason,dict_TotalPartitionalTime, totalTimeout)
def countPartitionalTime(readLogfileResultDict, methodName, timeUpperBound, timeLowerBound, partitionalNames):
    dict_stopReason = dict()
    dict_TotalPartitionalTime = dict()
    totalTimeout = 0
    dict_totalTime = readLogfileResultDict["dict_totalTime"]
    dict_methodName = readLogfileResultDict["dict_methodName"]
    dict_partitionalTime = readLogfileResultDict["dict_partitionalTime"]
    partitionalNameList = partitionalNames.split(";")
    for logid in dict_methodName:
        if methodName in dict_methodName[logid] and timeLowerBound < dict_totalTime[logid] and timeUpperBound > dict_totalTime[logid] :
            totalTimeout += 1
            stopReason = isExistingStop(dict_partitionalTime,partitionalNames, logid)            
            if stopReason!="noStop":
                if dict_stopReason.has_key(stopReason):
                    dict_stopReason[stopReason] += 1
                else:
                    dict_stopReason[stopReason] = 1
            else:
                thisPositionTime = 0
                lastPositionTime = 0
                for partitionalName in partitionalNameList:
                    thisPositionTime = dict_partitionalTime[partitionalName][logid]
                    timeCost = thisPositionTime - lastPositionTime 
                    if dict_TotalPartitionalTime.has_key(partitionalName):
                        dict_TotalPartitionalTime[partitionalName] += timeCost
                    else:
                        dict_TotalPartitionalTime[partitionalName] = timeCost
                    lastPositionTime = thisPositionTime
    dict_result = dict()
    dict_result["dict_stopReason"] = dict_stopReason
    dict_result["dict_TotalPartitionalTime"] = dict_TotalPartitionalTime
    dict_result["totalTimeout"] = totalTimeout 
    return dict_result

filename = "D:/server-trace.log"
partitionalNames = "getPackageInfo;getPackageCond;isExceedVip;getPackageStatus;getUserScore;getGameCode;getPackageDetail;putGameCode;updatePackageDetail;saveData;grabPackage;notifyCardSystemUserGetPackage"
requestStartFlag = "grabSelectTypePackageStart"
requestEndFlag = "grabCodeEnd"
timeUpperBound = 999999999
timeLowerBound = 0
methodName = "grabSelectTypePackage"
print "Start Process Logfine", filename
partitionalNames = partitionalNames + ";" + requestEndFlag
readLogfileResultDict = readLogfile(filename, partitionalNames, requestStartFlag, requestEndFlag)
analysisResultDict = countPartitionalTime(readLogfileResultDict, methodName, timeUpperBound, timeLowerBound, partitionalNames)
totalRequest = len(readLogfileResultDict["dict_methodName"])
totalTimeout = analysisResultDict["totalTimeout"]
print "totalRequest",totalRequest,"totalTimeout",totalTimeout
partitionalNameList = partitionalNames.split(";")
currentPosition = ""
lastPosition = requestStartFlag
print "cost time distribution"
for partitionalName in partitionalNameList:
    print " ",partitionalName,analysisResultDict["dict_TotalPartitionalTime"][partitionalName]
    lastPosition = partitionalName

print "stop position distribution"
for key in analysisResultDict["dict_stopReason"]:
    print " ",key, analysisResultDict["dict_stopReason"][key]

                    
                    
    











