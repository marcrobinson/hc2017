class CacheServer():
    capacity = None

    def __init__(self, ID):
        self.ID = ID
        self.videos = []
        self.remaining_size = self.capacity
        self.cache_server_connections = []

    def add_video(self, video):
        #if( video.size <= self.get_remaining_space()):
        if(video.size <= self.remaining_size):
            self.videos.append(video)
            self.remaining_size -= video.size

    def get_remaining_space(self):
        return self.remaining_size

        #occ = sum([v.size for v in self.videos])
        #return self.capacity - occ
