from VideoCache import *

class Output(object):
    
    def set_output_filename(self, filename):
        self.filename = filename

    def set_cache_list(self, cache_servers):
        self.cache_servers = cache_servers

    def output_file_data(self):
        file = open(self.filename, "w")

        file.write(str(len(self.cache_servers)) + "\n")

        for i in range(len(self.cache_servers)):
            line = ""
            cache_server = self.cache_servers[i]

            line += str(cache_server.ID)
            
            for i in range(len(cache_server.videos)):
                video = cache_server.videos[i]
                
                line += " " + str(video.ID)

            line += "\n"

            file.write(line)


if __name__ == "__main__":
    out = Output()
    out.set_output_filename("my_out.out")

    vid1 = Video(0, 30)
    vid2 = Video(1, 20)
    vid3 = Video(2, 80)
    vid4 = Video(3, 50)
    vid5 = Video(4, 30)

    cache_servers = [CacheServer(0), CacheServer(1), CacheServer(2), CacheServer(5)]
    cache_servers[0].videos = [vid1, vid2]
    cache_servers[1].videos = [vid4, vid5, vid2]
    cache_servers[2].videos = [vid3, vid1, vid5]

    out.set_cache_list(cache_servers)

    out.output_file_data()

    print("")
