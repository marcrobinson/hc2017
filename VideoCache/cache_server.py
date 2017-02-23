class CacheServer():
    capacity = None

    def __init__(self, ID):
        self.ID = ID
        self.videos = []


    def add_video(self, video):
        if( video.size < self.get_remaining_space()):
            self.videos.append(video)

    def get_remaining_space(self):
        occ = sum([v.size for v in self.videos])

        return self.capacity - occ
