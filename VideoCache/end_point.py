class Endpoint:
    def __init__(self, ID, data_center_latency):
        self.ID = ID
        self.data_center_latency = data_center_latency
        self.cache_server_connections = []

    # def get_connection(self, cs):
    #     if(cs in self.cache_server_connections_hash.keys()):
    #         return self.cache_server_connections_hash[cs]
    #     else:
    #         return None