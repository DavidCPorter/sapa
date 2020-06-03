import argparse
import os


class TestParam( object ):
    def __init__( self, host="", port=0, threads=1, http_pool=None, base_url="", ramp=1,
                  duration=1, conns=1, rand_req=False, max_rand_obj=1, req_dist="", poisson_lam=1.0,
                  gauss_mean=1.0, gauss_std=1.0, max_iters=5000, loop='closed', engine='' ):
        self.host         = host
        self.port         = port
        self.threads      = threads
        self.http_pool    = http_pool
        self.base_url     = base_url
        self.ramp         = ramp
        self.duration     = duration
        self.conns        = conns
        self.rand_req     = rand_req
        self.max_rand_obj = max_rand_obj
        self.req_dist     = req_dist
        self.poisson_lam  = poisson_lam
        self.gauss_mean   = gauss_mean
        self.gauss_std    = gauss_std
        self.max_iters    = max_iters
        self.loop         = loop
        self.engine       = engine
        return


def parse_commandline(cl_args):
    # Parse command line arguments
    parser = argparse.ArgumentParser( )
    parser.add_argument( "--threads", dest="threads", type=int, default=15,
                         help="Number of threads to use"  )
    parser.add_argument( "--host", dest="host", default="128.105.144.184",
                         help="Web server host name" )
    parser.add_argument( "--port", dest="port", type=int, default=9111,
                         help="Web server port number" )
    parser.add_argument( "--duration", dest="duration", type=float, default=20,
                         help="Duration of test in seconds" )
    parser.add_argument( "--ramp", dest="ramp", type=float, default=1,
                         help="Ramp time for duration-based testing" )

    parser.add_argument( "--size", dest="transfer_size", type=int, default=1024,
                         help="Total transfer size in bytes. Overrides duration-based settings" )

    parser.add_argument( "--connections", dest="conns", type=int, default=10,
                         help="Number of connections to use per thread" )

    parser.add_argument( "--shards", dest="shards", type=int, default=4,
                         help="Number of shards for collection" )

    parser.add_argument( "--replicas", dest="replicas", type=int, default=3,
                         help="Number of replicas for collection" )

    parser.add_argument( "--test-type", dest="test_type", choices=["duration","size"], default="duration",
                         help="Type of test to perform" )

    parser.add_argument( "--random", dest="rand_req", action="store_true", default=False,
                         help="Indicates that threads should perform random requests. Otherwise sequential requests are performed." )

    parser.add_argument( "--max-rand-obj", dest="max_rand_obj", type=int, default=1000,
                         help="Maximum number of objects from which clients will make random requests" )

    parser.add_argument( "--output-dir", dest="output_dir", default=os.path.dirname(os.path.realpath(__file__)),
                         help="Directory to store output CSV file." )

    parser.add_argument( "--req-dist", dest="req_dist", choices=["gauss", "poisson"], default="gauss",
                         help="Client wait time distribution type." )

    parser.add_argument( "--query", dest="query", choices=["client", "roundrobin"], default="client",
                         help="queries made using client or roundrobin" )
    parser.add_argument( "--loop", dest="loop", choices=["open", "closed"], default="closed",
                         help="run open or closed loop experiment")
    parser.add_argument( "--solrnum", dest="clustersize", default="4",
                        help="number of nodes running solr")
    parser.add_argument( "--instances", dest="instances", default=None,
                        help="number of solr instances running in each node")
    parser.add_argument( "--engine", dest="engine", default=None,
                        help="solr or elastic",choices=["solr", "elastic"])

    #just hardcoded a random generating query
    # parser.add_argument( "--query", dest="query", default="summary",
    #                      help="query string to run on Amazon reviews_rf2q" )

    main_args = parser.parse_args(cl_args)
    return main_args
