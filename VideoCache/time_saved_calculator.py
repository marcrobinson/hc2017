import logging
import numpy
#from numba import jit


def update_matrix(time_saved_matrix, request_to_video_map, video_id, videos_at_endpoint):

    time_saved_matrix[:,video_id] = 0

    for request in request_to_video_map[video_id]:
        # if request.video.ID != video_id:
        #     continue

        # check if video for this request is already in cache server
        # connected to requests endpoint
        skip = False
        for connection in request.endpoint.cache_server_connections:
            if (request.video in connection.cache_server.videos):

                skip = True
                break

        if (skip): continue

        #if(videos_at_endpoint[request.video.ID][request.endpoint.ID] == 1):continue

        for connection in request.endpoint.cache_server_connections:
            # if (request.video in connection.cache_server.videos):
            #     continue

            time_saved = 0.0
            # can we fit video on cs?
            if (connection.cache_server.get_remaining_space() >= request.video.size):
                time_saved = request.endpoint.data_center_latency - connection.latency
                time_saved *= request.num_of_requests

                # if(time_saved > max_saved):
                #    max_saved = time_saved
                # if(time_saved_matrix[connection.cache_server.ID][request.video.ID]>0):
                # print("Video from this server already added")

            time_saved_matrix[connection.cache_server.ID][request.video.ID] += time_saved


def calc_time_saved_matrix(request_decriptions, videos, cached_servers):
    '''

    matrix that is nvideos*ncacheservers containing total time saving of storing that video there
    across all requests


    :param request_decriptions:
    :param videos:
    :return:
    '''

    #need to store if we have registered an endpoint-video link...

    #if a video has already been placed in a cache attached to an endpoint

    time_saved_matrix = numpy.zeros((len(cached_servers),len(videos)))
    total_requests = 0
    for request in request_decriptions:

        #max_saved = 0.0

        total_requests += request.num_of_requests

        #maybe check here if the video is already on an endpoint, assuming
        #it has been placed there because it is the best location, ignore this request

        skip = False
        for connection in request.endpoint.cache_server_connections:
            if(request.video in connection.cache_server.videos):
                skip = True

        if(skip): continue

        for connection in request.endpoint.cache_server_connections:

            time_saved=0.0
            # can we fit video on cs?
            if(connection.cache_server.get_remaining_space() >= request.video.size):

                time_saved = request.endpoint.data_center_latency - connection.latency
                time_saved *= request.num_of_requests

            #if(time_saved > max_saved):
            #    max_saved = time_saved
            #if(time_saved_matrix[connection.cache_server.ID][request.video.ID]>0):
                #print("Video from this server already added")

            time_saved_matrix[connection.cache_server.ID][request.video.ID] += time_saved



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






