API_KEY = '6c6b183c887046e89d81df9552de02b1'

import requests


def get_routes_by_stop(stop_id):
    url = 'https://developer.cumtd.com/api/v2.2/json/getroutesbystop?key=' + API_KEY + '&stop_id=' + str(stop_id)
    response = requests.get(url)
    text = response.json()
    routes = []
    for route_dict in text['routes']:
        routes.append(route_dict['route_short_name'] + ' ' + route_dict['route_id'])
    return routes


def get_stop(stop_id):
    url = 'https://developer.cumtd.com/api/v2.2/json/getstop?key=' + API_KEY + '&stop_id=' + str(stop_id)
    response = requests.get(url)
    d = response.json()
    stop_dict = {}
    value = []
    lat_long = []
    for stop in d['stops'][0]['stop_points']:
        value.append(stop['stop_name'])
        lat_long.append((stop['stop_lat'], stop['stop_lon']))
    stop_dict['stop_names'] = value
    stop_dict['lat_lons'] = lat_long
    return stop_dict


def get_trip(trip_id):
    url = 'https://developer.cumtd.com/api/v2.2/json/gettrip?key=' + API_KEY + '&trip_id=' + str(trip_id)
    response = requests.get(url)
    text = response.json()
    trips = []
    for trip_dict in text['trips']:
        trips.append(trip_dict['route_id'] + ' ' + trip_dict['direction'] + ' ' + trip_dict['trip_headsign'])
    return trips


def get_stop_times_by_trip(trip_id):
    url = 'https://developer.cumtd.com/api/v2.2/json/getstoptimesbytrip?key=' + API_KEY + '&trip_id=' + str(trip_id)
    response = requests.get(url)
    text = response.json()
    stop_list = []
    for stop in text['stop_times']:
        stop_list.append((stop['arrival_time'], stop['departure_time'], stop['stop_point']['stop_name']))
    return stop_list


def get_trips_by_route(route_id):
    url = 'https://developer.cumtd.com/api/v2.2/json/gettripsbyroute?key=' + API_KEY + '&route_id=' + str(route_id)
    response = requests.get(url)
    text = response.json()
    routes = []
    for time in text['trips']:
        routes.append(time['shape_id'] + ' ' + time['route_id'] + ' ' + time['direction'] + ' ' + time['trip_headsign'])
    return routes


def get_stoptimes_bystop(stop_id, route_id=None, date=None):
    base_url = 'https://developer.cumtd.com/api/v2.2/json/getstoptimesbystop?key=' + API_KEY + '&stop_id=' + str(
        stop_id)
    if route_id is not None:
        base_url += '&route_id=' + str(route_id)
    if date is not None:
        base_url += '&date=' + str(date)
    response = requests.get(base_url)
    text = response.json()
    route_dict = {}
    for stop in text['stop_times']:
        time = stop['arrival_time']
        route = stop['trip']['route_id']
        if route not in route_dict:
            route_dict[route] = [time]
        else:
            route_dict[route].append(time)
    return route_dict
