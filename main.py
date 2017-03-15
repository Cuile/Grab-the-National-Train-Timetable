# -*- coding: utf-8 -*-
import grab
import shortest_path
import json

if __name__ == '__main__':
    # print(grab.grab_station_name())
    # print(grab.grab_train_list())
    # print(grab.grab_train_schedule('2017-03-13'))
    # ------------------------------------------------------------------------
    with open('train_schedule.json', 'r', encoding='utf-8') as ts:
        train_schedule = json.load(ts)
    for train in train_schedule:
        for station in range(len(train['train']['schedule']) - 1):
            print(train['train']['schedule'][station]['station_name'],
                  train['train']['schedule'][station + 1]['station_name'])
        exit()
