import logging
import numpy

def calc_time_saved_matrix(request_decriptions, videos, cached_servers):
    '''

    matrix that is nvideos*ncacheservers containing total time saving of storing that video there
    across all requests


    :param request_decriptions:
    :param videos:
    :return:
    '''

    time_saved_matrix = numpy.zeros((len(cached_servers),len(videos)))
    total_requests = 0
    for request in request_decriptions:
        for connection in request.endpoint.cache_server_connections:
            time_saved = request.endpoint.data_center_latency - connection.latency
            time_saved *= request.num_of_requests
            time_saved_matrix[connection.cache_server.ID][request.video.ID] += time_saved

        total_requests += request.num_of_requests

    return time_saved_matrix

def calculate_time_saved(request_descriptions):
    '''

    Used after assigning videos to cache

    score = sum over all requests, difference between latency from dc, vs latency from a cache

    :param videos:
    :param cache_servers:
    :param request_descriptions:
    :param endpoints:
    :return:
    '''

    total_time_saved = 0.0
    total_requests = 0.0
    for request in request_descriptions:
        min_latency = calc_min_latency_using_cache(request)
        if(min_latency == None):
            time_saved = 0.0
        else:

            time_saved = request.endpoint.data_center_latency - min_latency
            time_saved*=request.num_of_requests

        if(time_saved<0):
            time_saved = 0.0

        total_time_saved+=time_saved
        total_requests+=request.num_of_requests

    return total_time_saved, total_requests


def calc_min_latency_using_cache(request_description):
    '''

    calc min latency for a request

    :param request_description:
    :return:
    '''

    min = 1000000000

    for conn in request_description.endpoint.cache_server_connections:
        cs = conn.cache_server
        if(request_description.video in cs.videos):
            lat = conn.latency

            if(lat < min):
                min = lat
        else:
            continue


    if(min == 1000000000):return None
    else: return min






