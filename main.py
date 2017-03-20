# -*- coding: utf-8 -*-
import json

import grab
import shortest_path

if __name__ == '__main__':
    pass
    # print(grab.grab_station_name())
    # print(grab.grab_train_list())
    ts = grab.train_schedule()
    print(ts.get_train_schedule(d='2017-03-19', max_workers=10))
    print(shortest_path.get_edges('2017-03-19'))
    # ------------------------------------------------------------------------
    # with open('edges.json', 'r', encoding='utf-8') as e:
    #     edges = json.load(e)
    #
    # print(shortest_path.get_shortest_path(edges, '广州南', '北京西'))
    # print(shortest_path.get_shortest_path(edges, '广州东', '北京西'))
    # print(shortest_path.get_shortest_path(edges, '广州', '北京西'))
    # print(shortest_path.get_shortest_path(edges, '广州西', '北京西'))
    # print(shortest_path.get_shortest_path(edges, '广州北', '北京西'))
