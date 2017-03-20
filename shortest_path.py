# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta


# ------------------------------------------------------------------------

# Dijkstra算法——通过边实现松弛
# 指定一个点到其他各顶点的路径——单源最短路径

# 初始化图参数
# G = {1: {1: 0, 2: 1, 3: 12},
#      2: {2: 0, 3: 9, 4: 3},
#      3: {3: 0, 5: 5},
#      4: {3: 4, 4: 0, 5: 13, 6: 15},
#      5: {5: 0, 6: 4},
#      6: {6: 0}}

# 每次找到离源点最近的一个顶点，然后以该顶点为重心进行扩展
# 最终的到源点到其余所有点的最短路径
# 一种贪婪算法

def dijkstra_1(G, v0, INF=999):
    """
    使用 Dijkstra 算法计算指定点 v0 到图 G 中任意点的最短路径的距离
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


# edges = [
#     ("上海虹桥", "苏州北", 23),
#     ("苏州北", "南京南", 49),
#     ("南京南", "定远", 31),
#     ("定远", "徐州东", 51),
#     ("徐州东", "济南西", 63),
#     ("济南西", "沧州西", 46),
#     ("沧州西", "天津南", 22),
#     ("天津南", "廊坊", 18),
#     ("廊坊", "北京南", 21)
# ]
def dijkstra_2(edges, f, t):
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
# print("南京南 -> 廊坊:")
# print(dijkstra(edges, "南京南", "廊坊"))
# (11, ('G', ('F', ())))
# ------------------------------------------------------------------------


# distance = {(1, 2): 2,
#             (1, 3): 1,
#             (2, 3): 2,
#             (2, 4): 1,
#             (2, 5): 3,
#             (3, 4): 4,
#             (4, 5): 1,
#             (3, 6): 3,
#             (5, 7): 4,
#             (6, 7): 1}
maxcount = 7
stack = list()
dst = dict()
path = dict()


def dijkstra_3_Probe(sourcenode, desnode):
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
    dijkstra_3_Probe(item, desnode)


def dijkstra_3_searchPath(sourcenode, desnode):
    if sourcenode == desnode:
        return
    if desnode in path.keys():
        dijkstra_3_searchPath(sourcenode, path[desnode])
        print('path %d->%d' % (path[desnode], desnode))


# Probe(1, 7)
# print(path)
# {2: 1, 3: 1, 4: 2, 5: 4, 6: 3, 7: 6}
# searchPath(1, 5)
# path 1->2
# path 2->4
# path 4->5
# ------------------------------------------------------------------------
def get_edges(schedule_date):
    with open('get_train_schedule.json', 'r', encoding='utf-8') as ts:
        train_schedule = json.load(ts)

    edges = []
    year, month, day = schedule_date.split('-')
    for train in train_schedule:
        print(train['train']['station_train_code'])
        schedule = train['train']['schedule']
        for station in range(len(schedule) - 1):
            hour, minute = schedule[str(station)]['start_time'].split(':')
            start_time = datetime(int(year), int(month), int(day), int(hour), int(minute))
            hour, minute = schedule[str(station + 1)]['arrive_time'].split(':')
            arrive_time = datetime(int(year), int(month), int(day), int(hour), int(minute))
            if start_time > arrive_time:
                arrive_time += timedelta(days=1)
            edges.append((schedule[str(station)]['station_name'],
                          schedule[str(station + 1)]['station_name'],
                          int((arrive_time - start_time).seconds / 60)))

    with open('edges.json', 'w', encoding='utf-8') as fp:
        json.dump(edges, fp, ensure_ascii=False, sort_keys=True, indent=2)
    return True


def get_shortest_path(edges, start_station, arrive_station):
    try:
        path = dijkstra_2(edges, start_station, arrive_station)
        path = str(path)
        path = path.replace('(', '')
        path = path.replace(')', '')
        path = path.replace('\'', '')
        path = path.replace(' ', '')
        path = path.split(',')
        path.pop()
        path.reverse()
        return [path[-1], ' -> '.join(path[:-1])]
    except IndexError:
        return ['-']
