class CacheServerConnection:
    def __init__(self, cache_server, endpoint, cache_server_latency):
        self.cache_server = cache_server
        self.endpoint = endpoint
        self.latency = cache_server_latency