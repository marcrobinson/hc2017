'''

algorithm:


time_saving = max(calc_time_saving_matrix)

while time_saving > 0:

    calc_time_saving_matrix <- this accounts for servers being full

    pick video and server that gives biggest saving

    add video to server

    remove the request(s) that are satisfied by the current arrangement


'''
import os, numpy, copy
from VideoCache import data_reader, time_saved_calculator
from VideoCache.time_saved_calculator import calculate_time_saved
from VideoCache import output

import time


def iterative_method(fname):
    stime = time.time()


    file = os.path.join("../", "VideoCache", "input", fname+".in")
    #file = os.path.join("../", "VideoCache", "input", "me_at_the_zoo.in")
    reader = data_reader.DataReader(file)

    reader.read()

    # requests_to_vid_mapping = {}
    # requests_to_cs_mapping = {}
    #
    # for vid in reader.videos:
    #     requests_to_vid_mapping[vid] = []
    #
    # for cs in reader.cache_servers:
    #     requests_to_cs_mapping[cs] = []
    #
    # for req in reader.request_descriptions:
    #     requests_to_vid_mapping[req.video].append(req)
    #
    # for req in reader.request_descriptions:
    #     servers = [conn.cache_server for conn in req.endpoint.cache_server_connections]
    #     for server in servers: requests_to_cs_mapping[server].append(req)



    #reqs = copy.copy(reader.request_descriptions)

    max_time_save=1e50

    time_saving_matrix = time_saved_calculator.calc_time_saved_matrix(reader.request_descriptions,
                                                                      reader.videos,
                                                                      reader.cache_servers)

    request_to_video_map = {}

    for request in reader.request_descriptions:
        try:
            request_to_video_map[request.video.ID].append(request)
        except:
            request_to_video_map[request.video.ID] = []
            request_to_video_map[request.video.ID].append(request)

    #videos_at_endpoint = numpy.zeros((len(reader.videos), len(reader.endpoints)))
    videos_at_endpoint = None

    step = 0
    #delta = 10000
    while(max_time_save>0):
        #time_saving_matrix = time_saved_calculator.calc_time_saved_matrix(reader.request_descriptions,
        #                                                               reader.videos,
         #                                                                  reader.cache_servers)


        c_max_time_save = numpy.max(time_saving_matrix)
        #delta = max_time_save - c_max_time_save

        max_time_save = c_max_time_save

        server_id, video_id = numpy.unravel_index(numpy.argmax(time_saving_matrix),
                                                  time_saving_matrix.shape)

        server = reader.cache_servers[server_id]
        video = reader.videos[video_id]

        print("adding video {0} size {1}".format(video_id, video.size))

        server.add_video(video)

        #for conn in server.cache_server_connections:
        #    videos_at_endpoint[video.ID][conn.endpoint.ID] = 1


        # for req in reqs:
        #     if req in requests_to_cs_mapping[server] and req in requests_to_vid_mapping[video]:
        #         reqs.remove(req)

        # for req in reqs:
        #     if(does_request_involve_video_and_server(req, reader.videos[video_id], server)):
        #         reqs.remove(req)

        print(" max_time_save " + str(max_time_save))
        print("step {0}".format(step))
        #print(" delta " + str(delta))

        time_saved_calculator.update_matrix(time_saving_matrix, request_to_video_map, video_id, videos_at_endpoint)


        #print(" length_req " + str(len(reqs)))

        step+=1

    #print(time_saving_matrix)

    total_time_saved2, total_requests2 = calculate_time_saved(reader.request_descriptions)
    score2 = total_time_saved2 / total_requests2 * 1000
    print(" actual total time saved " + str(total_time_saved2))
    print(" actual score " + str(score2))

    strategy = "iterative"

    o = output.Output()
    o.set_cache_list(reader.cache_servers)
    o.set_output_filename(os.path.join("output", fname + "_" + strategy + ".out"))
    o.write()

    print("time taken "+str(time.time()-stime))


def does_request_involve_video_and_server(request_descriptor, video, server):

    if(request_descriptor.video == video):
        servers = [conn.cache_server for conn in request_descriptor.endpoint.cache_server_connections]
        if server in servers:
            return True
        else:
            return False
    else:
        return False




if __name__=="__main__":

    fname = ["videos_worth_spreading",
    "kittens",
    "me_at_the_zoo",
    "as",
    "trending_today"]

    #fname = ["me_at_the_zoo",]

    for f in fname:
        iterative_method(f)

