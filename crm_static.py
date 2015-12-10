# -*- coding: utf-8 -*-
import os
import sys
import time
import string

dict_totalTime = dict()
dict_tag = dict()
dict_getUserInfogetUserInfo = dict()
dict_getAlltMutilTypeActivityIdListBasedOnAppId = dict()
dict_getNewCommonActivitysInfoListByIdList = dict()
dict_setCommonActivityProperty = dict()
dict_allFinished = dict()


def guess_error_eason(dict_tag,dict_getUserInfogetUserInfo,dict_getAlltMutilTypeActivityIdListBasedOnAppId,dict_getNewCommonActivitysInfoListByIdList,dict_setCommonActivityProperty,dict_allFinished,key):
    if dict_tag.has_key(key)==False:
        return "unknown"
    if dict_getUserInfogetUserInfo.has_key(key)==False:
        print key
        return "userError"
    if dict_getAlltMutilTypeActivityIdListBasedOnAppId.has_key(key)==False:
        return "db&redisError"
    if dict_getNewCommonActivitysInfoListByIdList.has_key(key)==False:
        return "DBError"
    if dict_setCommonActivityProperty.has_key(key)==False:
        return "logicError"
    if dict_allFinished.has_key(key)==False:
        return "unknown"
    return "noError"
                                        
filename="D:/FFF.txt"
file_source = open(filename, "r")
for line in file_source.readlines():
    values = line.split(";")
    strTime = values[2]
    print values
    if strTime.isdigit() and dict_tag.has_key(values[1]):
        time = string.atoi(values[2])
        if dict_totalTime.has_key(values[1]):
            dict_totalTime[values[1]] = (dict_totalTime.get(values[1])>time) and  dict_totalTime.get(values[1]) or time
        else:
            dict_totalTime[values[1]] = time
        if "getUserInfo" in values[0] and "getMutilTypeActivityInfoList" in values[0]:
            dict_getUserInfogetUserInfo[values[1]]=time
        elif "getActivityByGameId" in values[0] and "getMutilTypeActivityInfoList" in values[0]:
            dict_getAlltMutilTypeActivityIdListBasedOnAppId[values[1]]=time
        elif "getPackagesBasedOnSelectedGameAndVipAccessLevel" in values[0] and "getMutilTypeActivityInfoList" in values[0]:
            dict_getNewCommonActivitysInfoListByIdList[values[1]]=time
        elif "total" in values[0] and "getMutilTypeActivityInfoList" in values[0]:
            dict_setCommonActivityProperty[values[1]]=time
        elif "total" in values[0] and "getMutilTypeActivityInfoList" in values[0]:
            dict_allFinished[values[1]]=time
    elif "###" in values[2]:
        dict_tag[values[1]]=values[0]

def split_time(dict_timeSplit, space, time):
    if dict_timeSplit.has_key(space):
        dict_timeSplit[space] += time
    else:
        dict_timeSplit[space] = time

dict_errorReason = dict()
dict_timeSplit = dict()
total_time_out = 0
for key in dict_tag:
    if "getPackageAndActivityCountResponse" in dict_tag[key]:
        total_time_out += 1
        errorReason = guess_error_eason(dict_tag,dict_getUserInfogetUserInfo,dict_getAlltMutilTypeActivityIdListBasedOnAppId,dict_getNewCommonActivitysInfoListByIdList,dict_setCommonActivityProperty,dict_allFinished,key)
        if errorReason!="noError":
            #print key, errorReason
            if dict_errorReason.has_key(errorReason):
                dict_errorReason[errorReason] += 1
            else:
                dict_errorReason[errorReason] = 1
        else:
            user_finish_time = dict_getUserInfogetUserInfo[key]
            dbredis_finish_time = dict_getAlltMutilTypeActivityIdListBasedOnAppId[key] - dict_getUserInfogetUserInfo[key]
            db_finish_time = dict_getNewCommonActivitysInfoListByIdList[key] - dict_getAlltMutilTypeActivityIdListBasedOnAppId[key]
            logic_finish_time = dict_setCommonActivityProperty[key] - dict_getNewCommonActivitysInfoListByIdList[key]
            final_finish_time = dict_allFinished[key] - dict_setCommonActivityProperty[key]
            split_time(dict_timeSplit, "user_finish_time", user_finish_time)
            split_time(dict_timeSplit, "dbredis_finish_time", dbredis_finish_time)
            split_time(dict_timeSplit, "db_finish_time", db_finish_time)
            split_time(dict_timeSplit, "logic_finish_time", logic_finish_time)
            split_time(dict_timeSplit, "final_finish_time", final_finish_time)

print "总请求量：",len(dict_tag),"总超时量：",total_time_out

for key in dict_errorReason:
    print key, dict_errorReason[key]

for key in dict_timeSplit:
    print key, dict_timeSplit[key]
        
file_source.close()
