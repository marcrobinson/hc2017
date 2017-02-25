import unittest,os
from VideoCache import data_reader

class ReadingTestCase(unittest.TestCase):
    def test_reading(self):
        file = os.path.join("../","VideoCache","input", "as.in")
        reader = data_reader.DataReader(file)

        reader.read()

        self.assertEqual(len(reader.videos), 5)
        self.assertEqual(len(reader.endpoints),2)
        self.assertEqual(len(reader.request_descriptions), 4)
        self.assertEqual(len(reader.cache_servers), 3)

        self.assertEqual(reader.cache_servers[0].capacity, 100)

        self.assertEqual(reader.videos[0].size, 50)
        self.assertEqual(reader.videos[1].size, 50)
        self.assertEqual(reader.videos[2].size, 80)
        self.assertEqual(reader.videos[3].size, 30)
        self.assertEqual(reader.videos[4].size, 110)

        self.assertEqual(reader.endpoints[0].data_center_latency, 1000)
        self.assertEqual(len(reader.endpoints[0].cache_server_connections), 3)

        self.assertEqual(reader.endpoints[0].cache_server_connections[0].latency, 100)
        self.assertEqual(reader.endpoints[0].cache_server_connections[0].cache_server.ID, 0)

        self.assertEqual(reader.endpoints[0].cache_server_connections[1].latency, 200)
        self.assertEqual(reader.endpoints[0].cache_server_connections[1].cache_server.ID, 2)

        self.assertEqual(reader.endpoints[0].cache_server_connections[2].latency, 300)
        self.assertEqual(reader.endpoints[0].cache_server_connections[2].cache_server.ID, 1)

        self.assertEqual(reader.endpoints[1].data_center_latency, 500)
        self.assertEqual(len(reader.endpoints[1].cache_server_connections), 0)

        self.assertEqual(len(reader.request_descriptions), 4)

        self.assertEqual(reader.request_descriptions[0].video.ID, 3)
        self.assertEqual(reader.request_descriptions[0].endpoint.ID, 0)
        self.assertEqual(reader.request_descriptions[0].num_of_requests, 1500)



if __name__ == '__main__':
    unittest.main()
