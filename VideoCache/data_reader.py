import os, numpy
from VideoCache import time_saved_calculator

from end_point import Endpoint
from cache_server import CacheServer
from cache_server_connection import CacheServerConnection
import time_saved_calculator
from video import Video
from request_description import RequestDescrption


class VideoCache:
    def __init__(self, filename):
        self.filename = filename

    def get_line_list(self, line):
        items = line.strip().split(" ")
        for i in range(len(items)):
            items[i] = int(items[i])
        return items

    def get_next_line_list(self):
        line = self.file.readline()
        return self.get_line_list(line)

    def get_data_model(self):
        data_model = DataModel()

        self.file = open(self.filename)
        self.num_of_videos, self.num_of_endpoints, self.num_of_request_descriptions, self.num_of_cache_servers, self.capacity_of_cache_server = self.get_next_line_list()

        CacheServer.capacity = self.capacity_of_cache_server

        data_model.cache_servers = []
        
        for i in range(self.num_of_cache_servers):
            data_model.cache_servers.append(CacheServer(i))

        data_model.videos = []
        
        video_sizes = self.get_next_line_list()
        for i in range(self.num_of_videos):
            data_model.videos.append(Video(i, video_sizes[i]))

        data_model.endpoints = []

        for i in range(self.num_of_endpoints):
            data_center_latency, num_of_cache_servers = self.get_next_line_list()
            endpoint = Endpoint(i, data_center_latency)
            endpoint.cache_server_connections = []
            for i in range(num_of_cache_servers):
                cache_server_ID, cache_server_latency = self.get_next_line_list()
                cache_server = data_model.cache_servers[cache_server_ID]
                cache_server_connection = CacheServerConnection(cache_server, endpoint, cache_server_latency)
                endpoint.cache_server_connections.append(cache_server_connection)
            data_model.endpoints.append(endpoint)

        data_model.request_descriptions = []

        for i in range(self.num_of_request_descriptions):
            video_ID, endpoint_ID, num_of_requests = self.get_next_line_list()
            video = data_model.videos[video_ID]
            endpoint = data_model.endpoints[endpoint_ID]
            data_model.request_descriptions.append(RequestDescrption(video, endpoint, num_of_requests))

        return data_model


if __name__ == "__main__":
    proc = VideoCache(os.path.join("input", "me_at_the_zoo.in"))
    data_model = proc.get_data_model()

    cs_video_val = time_saved_calculator.calc_benefit(data_model.request_descriptions, data_model.videos, data_model.cache_servers)



    print(cs_video_val)

    print("*********")

    print(numpy.sort(cs_video_val))

    print(numpy.argsort(cs_video_val))







