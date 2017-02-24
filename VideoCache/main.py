from data_reader import DataReader
from time_saved_calculator import calc_time_saved_matrix, calculate_time_saved
import output
import itertools
import time

import numpy,os

class Strategy():
    MOST_TIME_SAVED_FIRST="most_time_saved"
    PACKING="packing"


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

    total_time_saved = 0
    for server in reader.cache_servers:
        # sort by time saving
        times = time_saving_matrix[server.ID]

        if (strategy == Strategy.MOST_TIME_SAVED_FIRST):
            time_saved, video_ids = put_most_time_saved_first(times,
                                                  video_sizes,
                                                  server.capacity)

        # time_per_size = times/video_sizes
        #
        # video_ids2 = numpy.argsort(time_per_size)[::-1]
        #
        # #sorted_t = numpy.sort(times)[::-1]
        # video_ids = numpy.argsort(times)[::-1]

        # here could calculate times per video size

        total_time_saved+=time_saved

        [server.add_video(reader.videos[id]) for id in video_ids]

    print("{0} time for packing calc {1}".format(fname, time.time()- stime))

    o = output.Output()
    o.set_cache_list(reader.cache_servers)
    o.set_output_filename(os.path.join("output", fname + "_" + strategy + ".out"))
    o.write()

    print("{0} time for output {1}".format(fname, time.time()- stime))
    stime = time.time()

    #time_saved, total_requests = calculate_time_saved(reader.request_descriptions)

    total_requests = sum([nreq.num_of_requests for nreq in reader.request_descriptions])

    score = total_time_saved / total_requests * 1000

    print(fname+" "+str(time_saved))
    print(fname+" "+str(score))

    print("{0} time check time saved {1}".format(fname, time.time()- stime))
    stime = time.time()

if __name__ ==  "__main__":
    main()