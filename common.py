# -*- coding: utf-8 -*-
import time

start = startTime = end = endTime = bar = None


def timing_starts():
    global start, startTime
    start = time.clock()
    startTime = time.time()


def timing_ends(info):
    global end, endTime
    end = time.clock()
    endTime = time.time()
    print(info)
    print("-------------------------------------------------------------------------")
    print("CPU Running time: %fs" % (end - start))
    print("Script Running time: %fs" % (endTime - startTime))
    print("-------------------------------------------------------------------------")
