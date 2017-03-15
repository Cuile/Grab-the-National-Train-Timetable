# -*- coding: utf-8 -*-
import grab
import shortest_path
import json


def get_edges(schedule_date):
    with open('train_schedule.json', 'r', encoding='utf-8') as ts:
        train_schedule = json.load(ts)

    from datetime import datetime, timedelta
    edges = []
    year, month, day = schedule_date.split('-')
    for train in train_schedule:
        schedule = train['train']['schedule']
        for station in range(len(schedule) - 1):
            hour, minute = schedule[station]['start_time'].split(':')
            start_time = datetime(int(year), int(month), int(day), int(hour), int(minute))
            hour, minute = schedule[station + 1]['arrive_time'].split(':')
            arrive_time = datetime(int(year), int(month), int(day), int(hour), int(minute))
            if start_time > arrive_time:
                arrive_time += timedelta(days=1)
            edges.append((schedule[station]['station_name'],
                          schedule[station + 1]['station_name'],
                          int((arrive_time - start_time).seconds / 60)))

    with open('edges.json', 'w', encoding='utf-8') as fp:
        json.dump(edges, fp, ensure_ascii=False, sort_keys=True, indent=2)
    return True


def get_shortest_path(edges, start_station, arrive_station):
    try:
        path = shortest_path.dijkstra_2(edges, start_station, arrive_station)
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
        return ['无法到达']


if __name__ == '__main__':
    # print(grab.grab_station_name())
    # print(grab.grab_train_list())
    # print(grab.grab_train_schedule('2017-03-13'))
    # ------------------------------------------------------------------------
    # print(get_edges('2017-03-13'))
    with open('edges.json', 'r', encoding='utf-8') as e:
        edges = json.load(e)
    print(get_shortest_path(edges, '北京', '成都南'))
    print(get_shortest_path(edges, '成都南', '广元'))
