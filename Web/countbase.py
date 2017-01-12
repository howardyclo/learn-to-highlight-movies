#!/usr/bin/env python
# -*- coding=utf-8 -*-
import json
import os
import sys
from collections import defaultdict
import numpy as np
import codecs

def HightLight(Target):
    ## Get Json
    file = Target+".json"
    with open(file,'r',encoding="utf-8") as f:
        data = json.load(f)
    comments = sorted(data['comments'], key=lambda x: x['time'])
    
    ## Interval
    interval = 15
    start, end = int(comments[0]['time']), int(comments[-1]['time'])
    res = defaultdict(lambda: 0)
    maxtime = 0
    for comment in comments:
        time = int(comment['time'])
        if time > maxtime:
            maxtime = time

    pyl = 0#偏移量
    for comment in comments:
        time = int(comment['time'])
        if time%interval == 0 and time != 0:
            res[time] += 1
        else:
            if (time//interval+1)*interval > maxtime - pyl :
                res[maxtime-pyl] += 1
            else:
                res[(time//interval+1)*interval] += 1
            
    ## Count Process
    count = []
    for item in res:
        count.append(res[item])

    avg =np.mean(count)
    standard =np.std(count)
    
    ## Output
    Output = []
    threshold = avg+standard
    for item in res:
        if res[item]>= threshold:
            Output.append((item,res[item]))
    Output = sorted(Output, key=lambda x: x[1])
    Output = [(x-interval,x) for (x,y) in Output]
    return sorted(Output) #這個按照人氣篩選，再按照影片順序
    #return Output #這個按照人氣排序


    ## Output
    #Output = []
    #threshold = avg+standard
    #for item in res:
    #    if res[item]>= threshold:
    #        Output.append((item-interval,item))
    #return sorted(Output) 