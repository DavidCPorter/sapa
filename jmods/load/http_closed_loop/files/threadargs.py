import urllib3
import http.client
from testmodes import *
from clparsing import *
from benchstats import *


#returns a list passed to the threads to append (name,urls[i],req_start,req_finish,fct) for each request

thread_stats = ThreadStats()

def add_pool(main_args):
    http_pool = urllib3.connectionpool.HTTPConnectionPool( main_args.host,
                                                          port=main_args.port,
                                                          maxsize=(main_args.conns),
                                                          block=False)

    return http_pool

def add_conn(main_args):
    conn = http.client.HTTPConnection(main_args.host,main_args.port,timeout=10)

    return conn

def get_urls(test_param, terms, shards, replicas, clustersize, instances, query, engine):
    indexed_fields = ["reviewText","summary"]
    # no prefix for elastic... not sure how solr handles prefix, ut it works
    # prefix_url = "%s" % (test_param.base_url)

    prefix_url = ""

    urls = []
    # port 8983 is a benchamrk using direct solr instance queries
# single cluster
    csize = str(clustersize)

    if instances != None:
        csize = '9'+csize

    if query == "roundrobin" and engine == "solr":
        r = random.randint(1,len(terms))

        for i in range( test_param.max_iters ):
            i+=r
            term = terms[i%len(terms)].rstrip()
            field = indexed_fields[i%len(indexed_fields)]
            # q = '/solr/reviews_rf'+str(replicas)+'_s'+str(shards)+'_clustersize'+csize+'/select?q='+field+'%3A'+term+'&rows=10'
            # JANUS docker collection name is simply replicas_shards_index
            q = '/solr/'+str(shards)+'_'+str(replicas)+'_index/select?q='+field+'%3A'+term+'&rows=10'
            urls.append("%s%s" % (prefix_url, q))

# solrj
    elif query == "client":
        col = 'reviews_rf'+str(replicas)+'_s'+str(shards)+'_clustersize'+csize
        # port 9111 flow -> via solrJ
        # introduce randomness for each thread
        r = random.randint(1,len(terms))
        for i in range( test_param.max_iters ):
            i+=r
            term = terms[i%len(terms)].rstrip()
            field = indexed_fields[i%len(indexed_fields)]
            # q = 'solr/reviews_rf2q/select?q='+field+'%3A'+term+'&rows=10'
            urls.append( "/%s/%s/%s" % (field, term, col))
    elif engine == "elastic":
        index = 'reviews_rf'+str(replicas)+'_s'+str(shards)+'_csize'+csize
        r = random.randint(1,len(terms))
        for i in range( test_param.max_iters ):
            i+=r
            term = terms[i%len(terms)].rstrip()
            field = indexed_fields[i%len(indexed_fields)]
            # q = '/solr/reviews_rf'+str(replicas)+'_s'+str(shards)+'_clustersize'+csize+'/_search?q='+field+':'+term
            # testing with index reviews right now
            q='/'+index+'/_search?q='+field+':'+term
            urls.append("%s" % q)
    return urls

def get_terms():
    f = open('words.txt', 'r')
    terms = f.readlines()
    random.shuffle(terms)
    f.close()
    return terms


def create_threadargs(main_args,start_flag, stop_flag, gauss_mean, gauss_std, poisson_lam):
    """ returns  [ test_param, thread_stats]"""

    base_url = "http://%s:%s" % ( main_args.host, main_args.port)
    # return_list = queue.Queue()
    # return_list = ''
    # import pdb; pdb.set_trace()

    thread_stats.init_thread_stats(main_args.threads)

    print(main_args.host, main_args.port)
    # header = {'Connection':'Close'}

    if main_args.test_type == "size":
        target = size_based_test
        test_param = TestParam( host=main_args.host, port=main_args.port, threads=main_args.threads,
                                base_url=base_url, conns=main_args.conns, rand_req=main_args.rand_req,
                                max_rand_obj=main_args.max_rand_obj, req_dist=main_args.req_dist,
                                gauss_mean=gauss_mean, gauss_std=gauss_std, poisson_lam=poisson_lam, engine=main_args.engine )
    else:
        target = duration_based_test
        test_param = TestParam( host=main_args.host, port=main_args.port, threads=main_args.threads,
                                base_url=base_url, ramp=main_args.ramp, loop=main_args.loop,
                                duration=main_args.duration, conns=main_args.conns, rand_req=main_args.rand_req,
                                max_rand_obj=main_args.max_rand_obj, req_dist=main_args.req_dist,
                                gauss_mean=gauss_mean, gauss_std=gauss_std, poisson_lam=poisson_lam, engine=main_args.engine )

    thread_args = [ test_param, thread_stats]
    return thread_args
