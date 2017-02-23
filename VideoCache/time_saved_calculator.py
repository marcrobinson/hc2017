import logging


def calculate_time_saved(requests):
    '''

    score = sum over all requests, difference between latency from dc, vs latency from a cache

    :param videos:
    :param cache_servers:
    :param requests:
    :param endpoints:
    :return:
    '''

    total_time_saved = 0.0
    for request in requests:
        min_latency = calc_min_latency_using_cache(request)
        if(min_latency == None):
            time_saved = 0.0
        else:

            time_saved = request.endpoint.data_center_latency - min_latency

        total_time_saved+=time_saved

    return total_time_saved


def calc_min_latency_using_cache(request):
    '''

    calc min latency for a request

    :param request:
    :return:
    '''

    min = 1000000000

    for conn in request.endpoint.cache_server_connections:
        cs = conn.cache_server
        if(request.video in cs.videos):
            lat = conn.latency * request.nrequests

            if(lat < min):
                min = lat
        else:
            continue


    if(min == 1000000000):return None