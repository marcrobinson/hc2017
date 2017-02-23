import os

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
            endpoint = Endpoint(i, data_center_latency, num_of_cache_servers)
            endpoint.cache_server_connections = []
            for i in range(num_of_cache_servers):
                cache_server_ID, cache_server_latency = self.get_next_line_list()
                cache_server = data_model.cache_servers[cache_server_ID]
                cache_server_connection = CacheServerConnection(cache_server, endpoint, cache_server_latency)
                endpoint.cache_server_connections.append(cache_server_connection)
            data_model.endpoints.append(endpoint)



        print ""

class DataModel:
    pass

class CacheServer():
    def __init__(self, ID):
        self.ID = ID

class Video:
    def __init__(self, ID, size):
        self.ID = ID
        self.size = size

class Endpoint:
    def __init__(self, ID, data_center_latency, num_of_cache_servers):
        self.ID = ID
        self.data_center_latency = data_center_latency
        self.num_of_cache_servers = num_of_cache_servers 

class CacheServerConnection:
    def __init__(self, cache_server, endpoint, cache_server_latency):
        self.cache_server = cache_server
        self.endpoint = endpoint
        self.latency = cache_server_latency

if __name__ == "__main__":
    proc = VideoCache(os.path.join("input", "me_at_the_zoo.in"))
    data_model = proc.get_data_model()
