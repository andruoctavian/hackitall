from __future__ import print_function

import requests
import threading
import datetime
import json
import math

from .api_service import *

ONE_KILOMETER = 1000
TEN_KILOMETERS = 10000
TOTAL_DISTANCE = 0
MATRIX_SIZE = 5

start_lat = 0
start_lon = 0

w, h = MATRIX_SIZE, MATRIX_SIZE
mat = [[0 for x in range(w)] for y in range(h)]

dist = [[0 for x in range(w)] for y in range(h)]
for i in range(0, MATRIX_SIZE):
    for j in range(0, MATRIX_SIZE):
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
            mat[point['i']][point['j']] = 100

    def run(self):
        r = call_breezometer(str(self.point1['lat']), str(self.point1['lon']))
        self.set_matrix(r.json(), self.point1)
        if self.point2 is not None:
            r = call_breezometer(str(self.point2['lat']), str(self.point2['lon']))
            self.set_matrix(r.json(), self.point2)


def print_mat(this_mat, size):
    for i in range(0, size):
        for j in range(0, size):
            print(str(this_mat[i][j]) + ' ', end='')

        print('')


def get_time():
    return str(datetime.datetime.now())


def breezometer_route(google_response, grade):
    global start_lat, start_lon
    start_lat = google_response['routes'][0]['legs'][0]['start_location']['lat']
    start_lon = google_response['routes'][0]['legs'][0]['start_location']['lng']
    end_lat = google_response['routes'][0]['legs'][0]['end_location']['lat']
    end_lon = google_response['routes'][0]['legs'][0]['end_location']['lng']
    print('Start: ' + str(google_response["routes"][0]["legs"][0]['start_location']))
    print('End: ' + str(google_response["routes"][0]["legs"][0]['end_location']))
    distance = google_response['routes'][0]['legs'][0]['distance']['value']

    if start_lat == end_lat and start_lon == end_lon:
        return list()

    global MATRIX_SIZE
    if distance < ONE_KILOMETER:
        MATRIX_SIZE = 3
    elif distance < TEN_KILOMETERS:
        MATRIX_SIZE = 4

    global TOTAL_DISTANCE
    TOTAL_DISTANCE = get_distance(start_lat, start_lon, end_lat, end_lon)

    # Calculate matrix points
    print('Calculating matrix ' + get_time())
    lat_dist = (end_lat - start_lat) * (1.0 / (MATRIX_SIZE - 1))
    lon_dist = (end_lon - start_lon) * (1.0 / (MATRIX_SIZE - 1))

    print('Lat: ' + str(lat_dist))
    print('Lon: ' + str(lon_dist))
    t_lat = start_lat

    points = list()
    for i in range(0, MATRIX_SIZE):
        t_lon = start_lon
        for j in range(0, MATRIX_SIZE):
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

    if len(points) % 2 == 0:
        for i in range(0, len(points), 2):
            all_threads.append(MyThread(points[i], points[i+1]))
    else:
        for i in range(0, len(points) - 1, 2):
            all_threads.append(MyThread(points[i], points[i+1]))
        all_threads.append(MyThread(points[len(points) - 1], None))

    for th in all_threads:
        th.start()

    for th in all_threads:
        th.join()

    print('Done: ' + get_time())
    print('1: Extracted mat:')
    print_mat(mat, MATRIX_SIZE)

    dist[0][0] = 0
    print_mat(dist, MATRIX_SIZE)
    dijkstra(list(), 0, 0, grade, TOTAL_DISTANCE, points)
    print('2: Dijkstra distances')
    print_mat(dist, MATRIX_SIZE)
    print('3: Dijkstra prevs')
    print_mat(prev, MATRIX_SIZE)

    shortest_path = list()
    shortest_path_values = list()
    shortest_path_latlon = list()

    i = MATRIX_SIZE - 1
    j = MATRIX_SIZE - 1
    shortest_path.append([i, j])
    shortest_path_values.append(mat[i][j])
    while 1:
        shortest_path.append(prev[i][j])
        prev_i = i
        prev_j = j
        i = prev[prev_i][prev_j][0]
        j = prev[prev_i][prev_j][1]
        shortest_path_values.append(mat[i][j])
        if i == 0 and j == 0:
            break
        shortest_path_latlon.append([points[i * MATRIX_SIZE + j]['lat'], points[i * MATRIX_SIZE + j]['lon']])

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


def get_distance(point1_x, point1_y, point2_x, point2_y):
    return math.sqrt(math.pow((point1_x - point2_x), 2) + math.pow((point1_y - point2_y), 2))


def get_distance_points(point1_x, point1_y, point2_x, point2_y, points):
    return get_distance(points[point1_x * MATRIX_SIZE + point1_y]['lat'], points[point1_x * MATRIX_SIZE + point1_y]['lon'], points[point2_x * MATRIX_SIZE + point2_y]['lat'], points[point2_x * MATRIX_SIZE + point2_y]['lon'])


def get_distance_points2(point1_x, point1_y, point2_x, point2_y, points):
    return get_distance(point1_x, point1_y, points[point2_x * MATRIX_SIZE + point2_y]['lat'], points[point2_x * MATRIX_SIZE + point2_y]['lon'])


def complex_formula(slider, cur_x_1, cur_y_1, cur_x_2, cur_y_2, total_distance, total, points):
    return (100.0 - slider) * get_distance_points2(cur_x_1, cur_y_1, cur_x_2, cur_y_2, points) / float(total_distance) + ((slider * (total + mat[cur_x_2][cur_y_2])) / 100.0)


def dijkstra(visited, cur_x, cur_y, slider, total_dist, points):
    visited.append([cur_x, cur_y])
    global start_lon, start_lat

    total = dist[cur_x][cur_y]
    if cur_x + 1 < MATRIX_SIZE and dist[cur_x + 1][cur_y] > complex_formula(slider, start_lat, start_lon, cur_x + 1, cur_y, total_dist, total, points):
        dist[cur_x + 1][cur_y] = complex_formula(slider, start_lat, start_lon, cur_x + 1, cur_y, TOTAL_DISTANCE, total, points)
        prev[cur_x + 1][cur_y] = [cur_x, cur_y]

    if cur_y + 1 < MATRIX_SIZE and dist[cur_x][cur_y + 1] > complex_formula(slider, start_lat, start_lon, cur_x, cur_y + 1, total_dist, total, points):
        dist[cur_x][cur_y + 1] = complex_formula(slider, start_lat, start_lon, cur_x, cur_y + 1, TOTAL_DISTANCE, total, points)
        prev[cur_x][cur_y + 1] = [cur_x, cur_y]

    if cur_x - 1 >= 0 and dist[cur_x - 1][cur_y] > complex_formula(slider, start_lat, start_lon, cur_x - 1, cur_y, total_dist, total, points):
        dist[cur_x - 1][cur_y] = complex_formula(slider, start_lat, start_lon, cur_x - 1, cur_y, TOTAL_DISTANCE, total, points)
        prev[cur_x - 1][cur_y] = [cur_x, cur_y]

    if cur_y - 1 >= 0 and dist[cur_x][cur_y - 1] > complex_formula(slider, start_lat, start_lon, cur_x, cur_y - 1, total_dist, total, points):
        dist[cur_x][cur_y - 1] = complex_formula(slider, start_lat, start_lon, cur_x, cur_y - 1, TOTAL_DISTANCE, total, points)
        prev[cur_x][cur_y - 1] = [cur_x, cur_y]

    # Diagonals
    if cur_x + 1 < MATRIX_SIZE and cur_y + 1 < MATRIX_SIZE and dist[cur_x + 1][cur_y + 1] > complex_formula(slider, start_lat, start_lon, cur_x + 1, cur_y + 1, total_dist, total, points):
        dist[cur_x + 1][cur_y + 1] = complex_formula(slider, start_lat, start_lon, cur_x + 1, cur_y + 1, TOTAL_DISTANCE, total, points)
        prev[cur_x + 1][cur_y + 1] = [cur_x, cur_y]

    if cur_x + 1 < MATRIX_SIZE and cur_y - 1 >= 0 and dist[cur_x + 1][cur_y - 1] > complex_formula(slider, start_lat, start_lon, cur_x + 1, cur_y - 1, total_dist, total, points):
        dist[cur_x + 1][cur_y - 1] = complex_formula(slider, start_lat, start_lon, cur_x + 1, cur_y - 1, TOTAL_DISTANCE, total, points)
        prev[cur_x + 1][cur_y - 1] = [cur_x, cur_y]

    if cur_x - 1 >= 0 and cur_y - 1 >= 0 and dist[cur_x - 1][cur_y - 1] > complex_formula(slider, start_lat, start_lon, cur_x - 1, cur_y - 1, total_dist, total, points):
        dist[cur_x - 1][cur_y - 1] = complex_formula(slider, start_lat, start_lon, cur_x - 1, cur_y - 1, TOTAL_DISTANCE, total, points)
        prev[cur_x - 1][cur_y - 1] = [cur_x, cur_y]

    if cur_x - 1 >= 0 and cur_y + 1 < MATRIX_SIZE and dist[cur_x - 1][cur_y + 1] > complex_formula(slider, start_lat, start_lon, cur_x - 1, cur_y + 1, total_dist, total, points):
        dist[cur_x - 1][cur_y + 1] = complex_formula(slider, start_lat, start_lon, cur_x - 1, cur_y + 1, TOTAL_DISTANCE, total, points)
        prev[cur_x - 1][cur_y + 1] = [cur_x, cur_y]

    # Get min value not visited
    min = 99999
    sel_i = -1
    sel_j = -1
    for i in range(0, MATRIX_SIZE):
        for j in range(0, MATRIX_SIZE):
            if [i, j] not in visited and dist[i][j] < min:
                min = dist[i][j]
                sel_i = i
                sel_j = j
    if not len(visited) == (MATRIX_SIZE * MATRIX_SIZE):
        dijkstra(visited, sel_i, sel_j, slider, total_dist, points)
