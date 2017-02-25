from data_reader import DataReader
from time_saved_calculator import calc_time_saved_matrix, calculate_time_saved
import output
import itertools
import time

import numpy,os

class Strategy():
    MOST_TIME_SAVED_FIRST="most_time_saved"
    PACKING="packing"
    FACTOR_SIZE="factor_size"




def put_videos_in_server(time_saved, video_size, server_capacity):
    '''

    example method for putting videos in server

    :param time_saved: numpy array of time saved, index is video id
    :param video_size: numpy array of video size, index is video id
    :param server_capacity: capacity of server
    :return: time saved from this cache server, list of video IDs to put in server
    '''
    return 0, numpy.arange(0,len(video_size))


def put_most_time_saved_first(time_saved, video_size, server_capacity):
    '''
    return video ids that by putting most time savd first,
    does not consider packing into server capacity

    :param time_saved:
    :param video_size:
    :param server_capacity:
    :return:
    '''

    sorted_video_index = numpy.argsort(time_saved)[::-1]
    out_ids = []

    space = server_capacity

    total_time_saved = 0

    for vid in sorted_video_index:
        if(space>=video_size[vid]):
            out_ids.append(vid)
            space -= video_size[vid]
            total_time_saved+=time_saved[vid]

        if(space<0):
            break

    return total_time_saved, out_ids

def put_video_factor_size(time_saved, video_size, server_capacity):
    '''
    return video ids that by putting most time savd first,
    does not consider packing into server capacity

    :param time_saved:
    :param video_size:
    :param server_capacity:
    :return:
    '''

    sorted_video_index = numpy.argsort(time_saved/video_size)[::-1]
    out_ids = []

    space = server_capacity

    total_time_saved = 0

    for vid in sorted_video_index:
        if(space>=video_size[vid]):
            out_ids.append(vid)
            space -= video_size[vid]
            total_time_saved+=time_saved[vid]

        if(space<=0):
            break

    return total_time_saved, out_ids


sort_methods = {}
sort_methods[Strategy.FACTOR_SIZE] = put_video_factor_size
sort_methods[Strategy.MOST_TIME_SAVED_FIRST] = put_most_time_saved_first

def main():
    '''

    read input,

    calc time saved matrix

    for each cs (row),
        assign videos to cs based on criteria (i.e. most time saved first vs video size)

    write final video locations

    :return:
    '''

    fname = ["videos_worth_spreading",
    "kittens",
    "me_at_the_zoo",
    "as",
    "trending_today"]

    fname = [
              "me_at_the_zoo",]

    strategy = Strategy.MOST_TIME_SAVED_FIRST

    for f in fname:
        calc_video_locations(f, strategy)


def calc_video_locations(fname, strategy):

    stime = time.time()

    reader = DataReader(os.path.join("input", fname + ".in"))
    reader.read()

    print("{0} time for read {1}".format(fname, time.time()- stime))

    video_sizes = [v.size for v in reader.videos]

    stime = time.time()

    time_saving_matrix = calc_time_saved_matrix(reader.request_descriptions,
                                                reader.videos,
                                                reader.cache_servers)

    print("{0} time for matrix calc {1}".format(fname, time.time()- stime))
    stime = time.time()

    # recalc the matrix each time video is added to server

    # for i in range(0,10000):
    #
    #
    #
    #     sid, id = numpy.unravel_index(numpy.argmax(time_saving_matrix),time_saving_matrix.shape)
    #
    #     server = [s for s in reader.cache_servers if s.ID==sid][0]
    #
    #     server.add_video(reader.videos[id])
    #
    #     time_saving_matrix = calc_time_saved_matrix(reader.request_descriptions,
    #                                                 reader.videos,
    #                                                 reader.cache_servers)

    total_time_saved = 0
    for server in reader.cache_servers:
        # sort by time saving
        times = time_saving_matrix[server.ID]

        time_saved, video_ids = sort_methods[strategy](times,
                                                  video_sizes,
                                                  server.capacity)

        total_time_saved+=time_saved

        [server.add_video(reader.videos[id]) for id in video_ids]

    print("{0} time for packing calc {1}".format(fname, time.time()- stime))

    o = output.Output()
    o.set_cache_list(reader.cache_servers)
    o.set_output_filename(os.path.join("output", fname + "_" + strategy + ".out"))
    o.write()

    print("{0} time for output {1}".format(fname, time.time()- stime))
    stime = time.time()

    total_time_saved2, total_requests2 = calculate_time_saved(reader.request_descriptions)
    score2 = total_time_saved2 / total_requests2 * 1000
    print(fname + " actual total time saved " + str(total_time_saved2))
    print(fname + " actual score " + str(score2))

    # total_requests = sum([nreq.num_of_requests for nreq in reader.request_descriptions])
    # score = total_time_saved / total_requests * 1000
    #
    # print(fname+" "+str(total_time_saved))
    # print(fname+" "+str(score))

    print("{0} time check time saved {1}".format(fname, time.time()- stime))
    stime = time.time()

if __name__ ==  "__main__":
    main()