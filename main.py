# -*- coding: utf-8 -*-
import json
import requests


def grab(url):
    # 请求头
    headers = {
        'Host': 'kyfw.12306.cn',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        # 'If-Modified-Since': '0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8'}
    return requests.get(url, headers=headers, verify=False).text


def grab_station_name():
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
    r = grab(url)
    r = r.replace('var station_names =\'@', '')
    r = r.replace('\';', '')
    r = r.split('@')
    station_name = []
    for i in r:
        station_name.append(i.split('|'))
    with open('station_name.json', 'w') as fp:
        json.dump(station_name, fp, ensure_ascii=False, indent=4)
    return True


def grab_train_list():
    url = 'https://kyfw.12306.cn/otn/resources/js/query/train_list.js?scriptVer'
    r = grab(url)
    r = r.replace('var train_list =', '')
    train_list = json.loads(r)
    with open('train_list.json', 'w') as fp:
        json.dump(train_list, fp, ensure_ascii=False, indent=4)
    return True


def grab_train_schedule():
    url = 'https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no=240000K60909&from_station_telecode=BJP&to_station_telecode=VVP&depart_date=2017-03-07'


if __name__ == '__main__':
    print(grab_station_name())
    print(grab_train_list())
