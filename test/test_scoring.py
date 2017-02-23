import unittest
from VideoCache import time_saved_calculator
from VideoCache.VideoCache import Video, CacheServer, CacheServerConnection, Endpoint, RequestDescrption


class MyTestCase(unittest.TestCase):

    def test_time_saved_dc_faster(self):
        my_video = Video(0,100)
        my_endpoint = Endpoint(0,100)
        my_cache_server = CacheServer(0)
        my_cache_server.videos.append(my_video)
        my_connection = CacheServerConnection(my_cache_server,my_endpoint, 110)
        my_endpoint.cache_server_connections.append(my_connection)
        my_request = RequestDescrption(my_video, my_endpoint, 1)

        time_saved = time_saved_calculator.calculate_time_saved([my_request])

        self.assertEqual(0, time_saved)

    def test_time_saved_cs_faster(self):

        my_video = Video(0,100)
        my_endpoint = Endpoint(0,110)
        my_cache_server = CacheServer(0)
        my_cache_server.videos.append(my_video)
        my_connection = CacheServerConnection(my_cache_server, my_endpoint, 100)

        my_endpoint.cache_server_connections.append(my_connection)

        my_request = RequestDescrption(my_video, my_endpoint, 1)

        score = time_saved_calculator.calculate_time_saved([my_request])

        self.assertEqual(10, score)

    def test_calc_benefit(self):

        my_video = Video(0, 100)
        my_endpoint = Endpoint(0, 110)
        my_cache_server = CacheServer(0)
        my_cache_server.videos.append(my_video)
        my_connection = CacheServerConnection(my_cache_server, my_endpoint, 100)

        my_endpoint.cache_server_connections.append(my_connection)

        my_request = RequestDescrption(my_video, my_endpoint, 1)

        score = time_saved_calculator.calculate_time_saved([my_request])

        #self.assertEqual(10, score)
        cs_video_val = time_saved_calculator.calc_benefit([my_request],[my_video,],[my_cache_server])


        print(cs_video_val)

        self.assertEqual(cs_video_val[0][0], 10)


if __name__ == '__main__':
    unittest.main()
