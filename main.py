# -*- coding: utf-8 -*-
import json

import grab
import shortest_path

if __name__ == '__main__':
    # print(grab.grab_station_name())
    # print(grab.grab_train_list())
    print(grab.grab_train_schedule('2017-03-19'))
    # ------------------------------------------------------------------------
    # print(get_edges('2017-03-13'))
    # with open('edges.json', 'r', encoding='utf-8') as e:
    #     edges = json.load(e)

    # print(shortest_path.get_shortest_path(edges, '北京', '成都南'))
    # print(shortest_path.get_shortest_path(edges, '成都南', '广元'))
