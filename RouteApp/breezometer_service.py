from __future__ import print_function

import json
import requests
import threading
import datetime

from gogreen.settings import *


w, h = 5, 5
mat = [[0 for x in range(w)] for y in range(h)]

dist = [[0 for x in range(w)] for y in range(h)]
for i in range(0, 5):
    for j in range(0, 5):
        dist[i][j] = 99999
dist[0][0] = 0

prev = [[0 for x in range(w)] for y in range(h)]
prev[0][0] = [0, 0]


class MyThread(threading.Thread):
    def __init__(self, point1, point2):
        threading.Thread.__init__(self)
        self.point1 = point1
        self.point2 = point2

    @staticmethod
    def set_matrix(res, point):
        if 'breezometer_aqi' in res:
            mat[point['i']][point['j']] = res['breezometer_aqi']
        else:
            mat[point['i']][point['j']] = '100'

    def run(self):
        r = requests.get('https://api.breezometer.com/baqi/?lat=' + str(self.point1['lat']) + '&lon=' + str(self.point1['lon']) + '&key=' + BREEZOMETER_API_KEY +
                         '&fields=breezometer_aqi,country_aqi')

        self.set_matrix(r.json(), self.point1)
        if self.point2 is not None:
            r = requests.get('https://api.breezometer.com/baqi/?lat=' + str(self.point2['lat']) + '&lon=' + str(self.point2[
                'lon']) + '&key=' + BREEZOMETER_API_KEY +
                             '&fields=breezometer_aqi,country_aqi')
            self.set_matrix(r.json(), self.point2)


def print_5x5(this_mat):
    for i in range(0, 5):
        for j in range(0, 5):
            print(str(this_mat[i][j]) + ' ', end='')

        print('')


def get_time():
    return str(datetime.datetime.now())


def breezometer_route(google_response):
    start_lat = google_response['routes'][0]['legs'][0]['start_location']['lat']
    start_lon = google_response['routes'][0]['legs'][0]['start_location']['lng']
    end_lat = google_response['routes'][0]['legs'][0]['end_location']['lat']
    end_lon = google_response['routes'][0]['legs'][0]['end_location']['lng']
    print('Start: ' + str(google_response["routes"][0]["legs"][0]['start_location']))
    print('End: ' + str(google_response["routes"][0]["legs"][0]['end_location']))

    # Calculate matrix points
    print('Calculating matrix ' + get_time())
    lat_dist = (end_lat - start_lat) * 0.25
    lon_dist = (end_lon - start_lon) * 0.25

    print('Lat: ' + str(lat_dist))
    print('Lon: ' + str(lon_dist))
    t_lat = start_lat

    points = list()
    for i in range(0, 5):
        t_lon = start_lon
        for j in range(0, 5):
            points.append({'lat': t_lat,
                           'lon': t_lon,
                           'i': i,
                           'j': j})
            print(str(t_lat) + ' ' + str(t_lon) + ' _ ', end='')
            t_lon += lon_dist
        print('')
        t_lat += lat_dist

    # Set threads
    print('Setting threads: ' + get_time())
    all_threads = list()

    for i in range(0, len(points) - 1, 2):
        all_threads.append(MyThread(points[i], points[i+1]))
    all_threads.append(MyThread(points[24], None))

    for th in all_threads:
        th.start()

    for th in all_threads:
        th.join()

    print('Done: ' + get_time())
    print('1: Extracted mat:')
    print_5x5(mat)

    dist[0][0] = mat[0][0]
    dijkstra(list(), 0, 0)
    print('2: Dijkstra distances')
    print_5x5(dist)
    print('3: Dijkstra prevs')
    print_5x5(prev)

    shortest_path = list()
    shortest_path_values = list()
    shortest_path_latlon = list()

    i = 4
    j = 4
    shortest_path.append([i, j])
    shortest_path_values.append(mat[i][j])
    shortest_path_latlon.append([points[i * 5 + j]['lat'], points[i * 5 + j]['lon']])
    while 1:
        shortest_path.append(prev[i][j])
        prev_i = i
        prev_j = j
        i = prev[prev_i][prev_j][0]
        j = prev[prev_i][prev_j][1]
        shortest_path_values.append(mat[i][j])
        shortest_path_latlon.append([points[i * 5 + j]['lat'], points[i * 5 + j]['lon']])
        if i == 0 and j == 0:
            break

    shortest_path = list(reversed(shortest_path))
    shortest_path_values = list(reversed(shortest_path_values))
    shortest_path_latlon = list(reversed(shortest_path_latlon))
    print('4: Shortest path')
    print(shortest_path)
    print('5: Shortest path values')
    print(shortest_path_values)
    print('6: Shortest path values')
    print(shortest_path_latlon)

    return shortest_path_latlon


def list_append(lst, item):
    lst.append(item)
    return lst


def dijkstra(visited, cur_x, cur_y):
    visited.append([cur_x, cur_y])

    total = dist[cur_x][cur_y]
    if cur_x + 1 < 5 and dist[cur_x + 1][cur_y] > total + mat[cur_x + 1][cur_y]:
        dist[cur_x + 1][cur_y] = total + mat[cur_x + 1][cur_y]
        prev[cur_x + 1][cur_y] = [cur_x, cur_y]

    if cur_y + 1 < 5 and dist[cur_x][cur_y + 1] > total + mat[cur_x][cur_y + 1]:
        dist[cur_x][cur_y + 1] = total + mat[cur_x][cur_y + 1]
        prev[cur_x][cur_y + 1] = [cur_x, cur_y]

    if cur_x - 1 >= 0 and dist[cur_x - 1][cur_y] > total + mat[cur_x - 1][cur_y]:
        dist[cur_x - 1][cur_y] = total + mat[cur_x - 1][cur_y]
        prev[cur_x - 1][cur_y] = [cur_x, cur_y]

    if cur_y - 1 >= 0 and dist[cur_x][cur_y - 1] > total + mat[cur_x][cur_y - 1]:
        dist[cur_x][cur_y - 1] = total + mat[cur_x][cur_y - 1]
        prev[cur_x][cur_y - 1] = [cur_x, cur_y]

    # Diagonals
    if cur_x + 1 < 5 and cur_y + 1 < 5 and dist[cur_x + 1][cur_y + 1] > total + mat[cur_x + 1][cur_y + 1]:
        dist[cur_x + 1][cur_y + 1] = total + mat[cur_x + 1][cur_y + 1]
        prev[cur_x + 1][cur_y + 1] = [cur_x, cur_y]

    if cur_x + 1 < 5 and cur_y - 1 >= 0 and dist[cur_x + 1][cur_y - 1] > total + mat[cur_x + 1][cur_y - 1]:
        dist[cur_x + 1][cur_y - 1] = total + mat[cur_x + 1][cur_y - 1]
        prev[cur_x + 1][cur_y - 1] = [cur_x, cur_y]

    if cur_x - 1 >= 0 and cur_y - 1 >= 0 and dist[cur_x - 1][cur_y - 1] > total + mat[cur_x - 1][cur_y - 1]:
        dist[cur_x - 1][cur_y - 1] = total + mat[cur_x - 1][cur_y - 1]
        prev[cur_x - 1][cur_y - 1] = [cur_x, cur_y]

    if cur_x - 1 >= 0 and cur_y + 1 < 5 and dist[cur_x - 1][cur_y + 1] > total + mat[cur_x - 1][cur_y + 1]:
        dist[cur_x - 1][cur_y + 1] = total + mat[cur_x - 1][cur_y + 1]
        prev[cur_x - 1][cur_y + 1] = [cur_x, cur_y]

    # Get min value not visited
    min = 99999
    sel_i = -1
    sel_j = -1
    for i in range(0, 5):
        for j in range(0, 5):
            if [i, j] not in visited and dist[i][j] < min:
                min = dist[i][j]
                sel_i = i
                sel_j = j

    if not len(visited) == 25:
        dijkstra(visited, sel_i, sel_j)
