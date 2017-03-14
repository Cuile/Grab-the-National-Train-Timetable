# -*- coding: utf-8 -*-
import json
import requests
from pprint import pprint


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
        sn = i.split('|')
        sn = {'id': sn[5], 'telecode': sn[2], 'station_name': sn[1], 'pinyin': sn[3], 'initials': sn[4], 'pinyin_code': sn[0]}
        # station_name.append(json.dumps(sn, ensure_ascii=False, sort_keys=True))
        station_name.append(sn)
    with open('station_name.json', 'w', encoding='utf-8') as fp:
        json.dump(station_name, fp, ensure_ascii=False, sort_keys=True, indent=2)
    return True


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


def grab_train_schedule():
    train_schedule = []
    with open('station_name.json', 'r') as sn, open('train_list.json', 'r') as tl:
        station_name = json.load(sn)
        train_list = json.load(tl)
        ts_err = []
        for i in train_list:
            train_no = i['train_no']
            # print(i['train_no'], i['from_station'], i['to_station'])
            for j in station_name:
                if i['from_station'] == j['station_name']:
                    from_station_telecode = j['telecode']
                if i['to_station'] == j['station_name']:
                    to_station_telecode = j['telecode']
            # print(train_no, from_station_telecode, to_station_telecode)
            url = 'https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no=%s&from_station_telecode=%s&to_station_telecode=%s&depart_date=2017-03-13' % (train_no, from_station_telecode, to_station_telecode)
            print(url)
            ts = json.loads(grab(url))
            try:
                train = ts['data']
                ts.clear()
                ts['train'] = train
                ts['train']['schedule'] = ts['train']['data']
                del ts['train']['data']
                ts['train']['start_station_name'] = ts['train']['schedule'][0]['start_station_name']
                del ts['train']['schedule'][0]['start_station_name']
                ts['train']['end_station_name'] = ts['train']['schedule'][0]['end_station_name']
                del ts['train']['schedule'][0]['end_station_name']
                ts['train']['station_train_code'] = ts['train']['schedule'][0]['station_train_code']
                del ts['train']['schedule'][0]['station_train_code']
                ts['train']['train_class_name'] = ts['train']['schedule'][0]['train_class_name']
                del ts['train']['schedule'][0]['train_class_name']
                ts['train']['service_type'] = ts['train']['schedule'][0]['service_type']
                del ts['train']['schedule'][0]['service_type']
                train_schedule.append(ts)
            except IndexError as err:
                ts_err.append(ts)
    with open('train_schedule.json', 'w', encoding='utf-8') as fp:
        json.dump(train_schedule, fp, ensure_ascii=False, sort_keys=True, indent=2)
    return True


if __name__ == '__main__':
    # print(grab_station_name())
    # print(grab_train_list())
    # print(grab_train_schedule())
    # ------------------------------------------------------------------------
    # Dijkstra算法——通过边实现松弛
    # 指定一个点到其他各顶点的路径——单源最短路径

    # 初始化图参数
    G = {1: {1: 0, 2: 1, 3: 12},
         2: {2: 0, 3: 9, 4: 3},
         3: {3: 0, 5: 5},
         4: {3: 4, 4: 0, 5: 13, 6: 15},
         5: {5: 0, 6: 4},
         6: {6: 0}}


    # 每次找到离源点最近的一个顶点，然后以该顶点为重心进行扩展
    # 最终的到源点到其余所有点的最短路径
    # 一种贪婪算法

    def Dijkstra(G, v0, INF=999):
        """ 使用 Dijkstra 算法计算指定点 v0 到图 G 中任意点的最短路径的距离
            INF 为设定的无限远距离值
            此方法不能解决负权值边的图
        """
        book = set()
        minv = v0

        # 源顶点到其余各顶点的初始路程
        dis = dict((k, INF) for k in G.keys())
        dis[v0] = 0

        while len(book) < len(G):
            book.add(minv)  # 确定当期顶点的距离
            for w in G[minv]:  # 以当前点的中心向外扩散
                if dis[minv] + G[minv][w] < dis[w]:  # 如果从当前点扩展到某一点的距离小与已知最短距离
                    dis[w] = dis[minv] + G[minv][w]  # 对已知距离进行更新

            new = INF  # 从剩下的未确定点中选择最小距离点作为新的扩散点
            for v in dis.keys():
                if v in book: continue
                if dis[v] < new:
                    new = dis[v]
                    minv = v
        return dis


    # dis = Dijkstra(G, v0=1)
    # print(dis.values())
    # dict_values([0, 1, 8, 4, 13, 17])
    # ------------------------------------------------------------------------
    from collections import defaultdict
    from heapq import *

    edges = [
        ("上海虹桥", "苏州北", 23),
        ("苏州北", "南京南", 49),
        ("南京南", "定远", 31),
        ("定远", "徐州东", 51),
        ("徐州东", "济南西", 63),
        ("济南西", "沧州西", 46),
        ("沧州西", "天津南", 22),
        ("天津南", "廊坊", 18),
        ("廊坊", "北京南", 21)
    ]


    def dijkstra(edges, f, t):
        g = defaultdict(list)
        for l, r, c in edges:
            g[l].append((c, r))

        q, seen = [(0, f, ())], set()
        while q:
            (cost, v1, path) = heappop(q)
            if v1 not in seen:
                seen.add(v1)
                path = (v1, path)
                if v1 == t:
                    return (cost, path)

                for c, v2 in g.get(v1, ()):
                    if v2 not in seen:
                        heappush(q, (cost + c, v2, path))

        return float("inf")


    # print("=== Dijkstra ===")
    # print(edges)
    # print("A -> E:")
    # print(dijkstra(edges, "A", "E"))
    # (14, ('E', ('B', ('A', ()))))
    print("南京南 -> 廊坊:")
    print(dijkstra(edges, "南京南", "廊坊"))
    # (11, ('G', ('F', ())))
    # ------------------------------------------------------------------------

    distance = {(1, 2): 2,
                (1, 3): 1,
                (2, 3): 2,
                (2, 4): 1,
                (2, 5): 3,
                (3, 4): 4,
                (4, 5): 1,
                (3, 6): 3,
                (5, 7): 4,
                (6, 7): 1}
    maxcount = 7
    stack = list()
    dst = dict()
    path = dict()


    def Probe(sourcenode, desnode):
        if sourcenode == desnode: return
        stack.append(sourcenode)
        for i in range(1, maxcount + 1):
            if (sourcenode, i) in distance.keys() and i not in stack:
                if (dst.get(sourcenode, 0) + distance[(sourcenode, i)] < dst.get(i, 1000)):
                    dst[i] = dst.get(sourcenode, 0) + distance[(sourcenode, i)]
                    path[i] = sourcenode
        if sourcenode in dst.keys():
            del dst[sourcenode]
        if not len(dst.keys()):
            return True
        item = sorted(dst.items(), key=lambda d: d[1])[0][0]
        Probe(item, desnode)


    def searchPath(sourcenode, desnode):
        if sourcenode == desnode:
            return
        if desnode in path.keys():
            searchPath(sourcenode, path[desnode])
            print('path %d->%d' % (path[desnode], desnode))


            # Probe(1, 7)
            # print(path)
            # {2: 1, 3: 1, 4: 2, 5: 4, 6: 3, 7: 6}
            # searchPath(1, 5)
            # path 1->2
            # path 2->4
            # path 4->5
            # ------------------------------------------------------------------------
