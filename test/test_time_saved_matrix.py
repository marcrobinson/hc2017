import unittest,os, numpy, copy
from VideoCache import data_reader, time_saved_calculator
from VideoCache.time_saved_calculator import calculate_time_saved

class TimeSavedMatrixTestCase(unittest.TestCase):
    def test_matrix(self):
        file = os.path.join("../","VideoCache","input", "videos_worth_spreading.in")
        reader = data_reader.DataReader(file)

        reader.read()

        reqs = copy.copy(reader.request_descriptions)

        while(len(reqs)>0):
            time_saving_matrix = time_saved_calculator.calc_time_saved_matrix(reqs,
                                                                              reader.videos,
                                                                              reader.cache_servers)

            print(time_saving_matrix)

            ssum = numpy.sum(time_saving_matrix)
            if(ssum<1e-6):
                break

            sid, id = numpy.unravel_index(numpy.argmax(time_saving_matrix),time_saving_matrix.shape)

            print(sid)
            print(id)

            server = [s for s in reader.cache_servers if s.ID == sid][0]

            server.add_video(reader.videos[id])

            newreqs = []
            for req in reqs:
                req_met = False
                if(req.video.ID == id):
                    for conn in req.endpoint.cache_server_connections:
                        if(conn.cache_server.ID == sid):
                            req_met = True
                            break

                if not req_met:
                    newreqs.append(req)

            reqs = newreqs

        total_time_saved2, total_requests2 = calculate_time_saved(reader.request_descriptions)
        score2 = total_time_saved2 / total_requests2 * 1000
        print(" actual total time saved " + str(total_time_saved2))
        print(" actual score " + str(score2))


        #
        # time_saving_matrix = time_saved_calculator.calc_time_saved_matrix(reqs,
        #                                                                   reader.videos,
        #                                                                   reader.cache_servers)
        #
        # print(time_saving_matrix)
        #
        # sid, id = numpy.unravel_index(numpy.argmax(time_saving_matrix), time_saving_matrix.shape)
        #
        # print(sid)
        # print(id)


if __name__ == '__main__':
    unittest.main()
