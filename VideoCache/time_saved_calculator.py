import logging
import numpy

def calculate_time_saved(request_descriptions):
    '''

    score = sum over all requests, difference between latency from dc, vs latency from a cache

    :param videos:
    :param cache_servers:
    :param request_descriptions:
    :param endpoints:
    :return:
    '''

    total_time_saved = 0.0
    for request in request_descriptions:
        min_latency = calc_min_latency_using_cache(request)
        if(min_latency == None):
            time_saved = 0.0
        else:

            time_saved = request.endpoint.data_center_latency - min_latency

        if(time_saved<0):
            time_saved = 0.0

        total_time_saved+=time_saved

    return total_time_saved


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
            lat = conn.latency * request_description.num_of_requests

            if(lat < min):
                min = lat
        else:
            continue


    if(min == 1000000000):return None
    else: return min


#def find_best_location_for_video():


def calc_benefit(request_decriptions, videos, cached_servers):
    '''

    array that is nvideos*ncacheservers containing benefit of storing that video there


    :param request_decriptions:
    :param videos:
    :return:
    '''

    cs_video_val = numpy.zeros((len(cached_servers),len(videos)))



    for cs in cached_servers:
        for video in videos:
            total_time_saved = 0

            for request in request_decriptions:
                if(request.video == video):

                    conn = request.endpoint.get_connection(cs)

                    if(conn!=None):
                        #calc benefit of request.video being in the cs

                        total_lat = request.endpoint.get_connection(cs).latency * request.num_of_requests

                        time_saved = request.endpoint.data_center_latency - total_lat

                        total_time_saved+=time_saved



            cs_video_val[cs.ID, request.video.ID] = total_time_saved




        return cs_video_val



