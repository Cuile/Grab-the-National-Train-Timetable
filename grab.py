# -*- coding: utf-8 -*-
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta

import requests

import common


# ------------------------------------------------------------------------


def grab(url):
    requests.packages.urllib3.disable_warnings()
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
    try:
        return requests.get(url, headers=headers, verify=False, timeout=15).text
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
        print(url)
        return '["timeout"]'


# ------------------------------------------------------------------------


def grab_station_name():
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
    r = grab(url)
    r = r.replace('var station_names =\'@', '')
    r = r.replace('\';', '')
    r = r.split('@')
    station_name = []
    for i in r:
        sn = i.split('|')
        sn = {'id': sn[5], 'telecode': sn[2], 'station_name': sn[1], 'pinyin': sn[3], 'initials': sn[4],
              'pinyin_code': sn[0]}
        station_name.append(sn)
    with open('station_name.json', 'w', encoding='utf-8') as fp:
        json.dump(station_name, fp, ensure_ascii=False, sort_keys=True, indent=2)
    return True


# ------------------------------------------------------------------------


def grab_train_list():
    url = 'https://kyfw.12306.cn/otn/resources/js/query/train_list.js'
    r = grab(url)
    r = r.replace('var train_list =', '')
    d = json.loads(r)
    train_list = []
    for key in d:
        for i in d[key]:
            for j in d[key][i]:
                j['station_train_code'] = j['station_train_code'].replace('(', '|')
                j['station_train_code'] = j['station_train_code'].replace(')', '|')
                j['station_train_code'] = j['station_train_code'].replace('-', '|')
                j['station_train_code'] = j['station_train_code'].split('|')
                j['train_code'] = j['station_train_code'][0]
                j['from_station'] = j['station_train_code'][1]
                j['to_station'] = j['station_train_code'][2]
                del j['station_train_code']
                train_list.append(json.dumps(j, ensure_ascii=False, sort_keys=True))
    train_list = list(set(train_list))
    for i in train_list:
        train_list[train_list.index(i)] = json.loads(i)
    with open('train_list.json', 'w', encoding='utf-8') as fp:
        json.dump(train_list, fp, ensure_ascii=False, sort_keys=True, indent=2)
    return True


# ------------------------------------------------------------------------
class train_schedule():
    def get_train_schedule(self, d, max_workers):
        # self.grab_train_schedule(d, max_workers)
        self.parse_train_schedule()

    def parse_train_schedule(self):
        with open('train_schedule.json', 'r', encoding='utf-8') as ts:
            train_schedule = json.load(ts)

        get_train_schedule = []
        get_train_schedule_err = []

        for ts in train_schedule:
            try:
                train = ts['data']
                ts.clear()
                ts['train'] = train

                ts['train']['schedule'] = ts['train']['data']
                del ts['train']['data']

                ts['train']['start_station_name'] = ts['train']['schedule'][0][
                    'start_station_name']
                del ts['train']['schedule'][0]['start_station_name']

                ts['train']['end_station_name'] = ts['train']['schedule'][0]['end_station_name']
                del ts['train']['schedule'][0]['end_station_name']

                ts['train']['station_train_code'] = ts['train']['schedule'][0][
                    'station_train_code']
                del ts['train']['schedule'][0]['station_train_code']

                ts['train']['train_class_name'] = ts['train']['schedule'][0]['train_class_name']
                del ts['train']['schedule'][0]['train_class_name']

                ts['train']['service_type'] = ts['train']['schedule'][0]['service_type']
                del ts['train']['schedule'][0]['service_type']

                ts['train']['s'] = sorted(ts['train']['schedule'], key=lambda x: x['station_no'])
                ts['train']['schedule'] = {}
                schedule_index = 0
                for td in ts['train']['s']:
                    ts['train']['schedule'].update({schedule_index: td})
                    schedule_index += 1
                del ts['train']['s']

                get_train_schedule.append(ts)

            except (IndexError, TypeError, json.decoder.JSONDecodeError):
                pass

        with open('get_train_schedule.json', 'w', encoding='utf-8') as fp:
            json.dump(get_train_schedule, fp, ensure_ascii=False, sort_keys=True, indent=2)

    def grab_train_schedule_callback(self, url):
        try:
            ts = json.loads(grab(url))
            # print(ts)
            return [True, ts]
        except json.decoder.JSONDecodeError:
            # print(ts)
            return [False, ts]

    def grab_train_schedule(self, d, max_workers):
        common.timing_starts()

        with open('station_name.json', 'r', encoding='utf-8') as sn:
            station_name = json.load(sn)
        with open('train_list.json', 'r', encoding='utf-8') as tl:
            train_list = json.load(tl)

        year, month, day = d.split('-')
        start_time = date(int(year), int(month), int(day))
        # dates = [
        #     start_time - timedelta(days=3),
        #     start_time - timedelta(days=2),
        #     start_time - timedelta(days=1),
        #     start_time,
        #     start_time + timedelta(days=1),
        #     start_time + timedelta(days=2),
        #     start_time + timedelta(days=3)
        # ]
        dates = [start_time]
        urls = []
        for d in dates:
            for i in train_list:
                train_no = i['train_no']
                for j in station_name:
                    if i['from_station'] == j['station_name']:
                        from_station_telecode = j['telecode']
                    if i['to_station'] == j['station_name']:
                        to_station_telecode = j['telecode']
                urls.append(
                    'https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no=%s&from_station_telecode=%s&to_station_telecode=%s&depart_date=%s' % (
                        train_no,
                        from_station_telecode,
                        to_station_telecode,
                        d.isoformat()
                    ))

        train_schedule = []
        train_schedule_err = []
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            for i in pool.map(self.grab_train_schedule_callback, urls):
                if i[0]:
                    train_schedule.append(i[1])
                else:
                    train_schedule_err.append(i[1])

        with open('train_schedule.json', 'w', encoding='utf-8') as fp:
            json.dump(train_schedule, fp, ensure_ascii=False, sort_keys=True, indent=2)

        common.timing_ends('抓取列车时刻表')

        return True
