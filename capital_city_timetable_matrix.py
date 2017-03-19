# -*- coding: utf-8 -*-

from pprint import pprint
import json
from concurrent.futures import ProcessPoolExecutor

import common
import shortest_path


# ------------------------------------------------------------------------
def compute_matrix_row(departure, provincial_capital_station, edges):
    temp = [departure[0] + ' ' + departure[1]]
    for destination in provincial_capital_station:
        try:
            temp.append(format(int(shortest_path.get_shortest_path(edges, departure[1], destination[1])[0]) / 60, '0.1f'))
        except ValueError:
            temp.append('无法到达')
    return temp


def compute_matrix_row_when_done(r):
    timetable_matrix.append(r.result())


# ------------------------------------------------------------------------
if __name__ == '__main__':
    common.timing_starts()
    provincial_capital = [
        ['安徽省', '合肥'],
        ['北京市', '北京'],
        ['重庆市', '重庆'],
        ['福建省', '福州'],
        ['甘肃省', '兰州'],
        ['广东省', '广州'],
        ['广西自治区', '南宁'],
        ['贵州省', '贵阳'],
        ['海南省', '海口'],
        ['河北省', '石家庄'],
        ['河南省', '郑州'],
        ['黑龙江省', '哈尔滨'],
        ['湖北省', '武汉'],
        ['湖南省', '长沙'],
        ['吉林省', '长春'],
        ['江苏省', '南京'],
        ['江西省', '南昌'],
        ['辽宁省', '沈阳'],
        ['内蒙古自治区', '呼和浩特'],
        ['宁夏自治区', '银川'],
        ['青海省', '西宁'],
        ['山东省', '济南'],
        ['山西省', '太原'],
        ['陕西省', '西安'],
        ['上海市', '上海'],
        ['四川省', '成都'],
        ['天津市', '天津'],
        ['西藏自治区', '拉萨'],
        ['新疆自治区', '乌鲁木齐'],
        ['云南省', '昆明'],
        ['浙江省', '杭州'],
        ['香港(特别行政区)', '香港'],
        ['澳门(特别行政区)', '澳门'],
        ['台湾省', '台北']
    ]
    provincial_capital_station = []

    with open('station_name.json', 'r', encoding='utf-8') as sn:
        station_name = json.load(sn)

    for city in provincial_capital:
        for station in station_name:
            try:
                station['station_name'].index(city[1])
                provincial_capital_station.append([city[0], station['station_name']])
            except ValueError:
                pass
    common.timing_ends('生成省会城市列表')
    # ------------------------------------------------------------------------
    common.timing_starts()

    with open('edges.json', 'r', encoding='utf-8') as e:
        edges = json.load(e)

    timetable_matrix = []

    temp = ['站名']
    for station in provincial_capital_station:
        temp.append(station[0] + ' ' + station[1])
    timetable_matrix.append(temp)

    with ProcessPoolExecutor() as pool:
        for departure in provincial_capital_station:
            future_result = pool.submit(compute_matrix_row, departure, provincial_capital_station, edges)
            future_result.add_done_callback(compute_matrix_row_when_done)

    common.timing_ends('生成省会城市之间，列车运行时间矩阵')
    # ------------------------------------------------------------------------
    for row in timetable_matrix:
        r = ''
        for item in row:
            r += str(item) + '\t'
        print(r)
