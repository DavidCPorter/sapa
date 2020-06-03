import numpy as np
import queue
import sys


class WebStats( object ):
    def __init__( self, tot_bytes=0, tot_requests=0, tot_responses=0, tot_errors=0,
                  avg_lat=0.0, duration=0.0, bw=0.0, stddev_lat=0.0,
                  min_lat=0.0, max_lat=0.0, nine_nine=0.0, nine_zero=0.0 ):
        self.tot_bytes    = tot_bytes
        self.tot_requests = tot_requests
        self.tot_responses = tot_responses
        self.tot_errors   = tot_errors
        self.avg_lat      = avg_lat
        self.stddev_lat   = stddev_lat
        self.min_lat      = min_lat
        self.max_lat      = max_lat
        self.duration     = duration
        self.bw           = bw
        self.nine_nine =    nine_nine
        self.nine_zero =    nine_zero


        return

class ThreadStats( object ):
    def __init__( self, requests=[], responses=[], byte_count=[], errors=[],
                  avg_lat=[], duration=0.0, ninenine=[], ninezero=[] ):
        self.requests   = requests
        self.responses  = responses
        self.byte_count = byte_count
        self.errors     = errors
        self.avg_lat    = avg_lat
        self.duration   = duration
        self.nine_nine = ninenine
        self.nine_zero = ninezero
        return

    def init_thread_stats(self, num):
        for i in range( num ):
            self.responses.append( 0 )
            self.requests.append( 0 )
            self.byte_count.append( 0 )
            self.errors.append( 0 )
            self.avg_lat.append( 0.0 )
            self.nine_nine.append( 0.0 )
            self.nine_zero.append( 0.0 )




def calc_web_stats( main_args, thread_stats ):
    """ Calculate:
        Average latency per thread
        Minimum latency over all threads
        Maximum latency over all threads
        Standard deviation in latency
        Total transfer size
        Bandwidth
        Total number of requests
        Number of requests per second
        Total number of errors
    """
    # Reorganize thread statistics for processing
    thread_stats.responses  = np.array( thread_stats.responses  )
    thread_stats.requests   = np.array( thread_stats.requests  )
    thread_stats.byte_count = np.array( thread_stats.byte_count )
    thread_stats.errors     = np.array( thread_stats.errors     )
    thread_stats.avg_lat    = np.array( thread_stats.avg_lat    )
    thread_stats.nine_nine    = np.array( thread_stats.nine_nine    )
    thread_stats.nine_zero    = np.array( thread_stats.nine_zero    )


    # Calculate average latency per thread
    avg_lat    = np.average( thread_stats.avg_lat )
    # calcluate 99 tail
    ninenine = np.average(thread_stats.nine_nine)
    # calculate 90 tail
    ninezero = np.average(thread_stats.nine_zero)

    # Calculate standard deviation in latency
    stddev_lat = np.std( thread_stats.avg_lat     ) * 100.0
    # Calculate minimum latency over all threads
    min_lat    = np.amin( thread_stats.avg_lat )
    # Calculate maximum latency over all threads
    max_lat    = np.amax( thread_stats.avg_lat )
    # Calculate total transfer size
    tot_bytes  = np.sum( thread_stats.byte_count  )
    # Caclulate bandwidth
    bw           = np.divide( tot_bytes, thread_stats.duration    )
    # avg of the p95 tail responses
    tot_requests = np.average( thread_stats.requests )
    # sum across threads of total number of responses per second
    tot_res_proc = np.sum( thread_stats.responses )
    # tot_res_proc = qps per processes
    # tot_res_proc = np.divide(main_args.threads, tot_responses)
    # Calculate total number of errors
    tot_errors   = np.sum( thread_stats.errors )

    web_stats = WebStats( tot_bytes=tot_bytes, tot_requests=tot_requests, tot_responses=tot_res_proc, tot_errors=tot_errors,
                          avg_lat=avg_lat, stddev_lat=stddev_lat, min_lat=min_lat, max_lat=max_lat,
                          duration=thread_stats.duration, bw=bw, nine_nine=ninenine, nine_zero=ninezero)

    return web_stats

def convert_units( web_stats ):
    """ Adjust metrics to appropriate units """
    ms_p_s = 1000.0
    MB_p_B = 1024 * 1024
    bits_p_B = 8

    web_stats.tot_bytes /= MB_p_B
    web_stats.tot_requests *= ms_p_s
    web_stats.avg_lat *= ms_p_s
    web_stats.min_lat *= ms_p_s
    web_stats.max_lat *= ms_p_s
    web_stats.nine_zero *= ms_p_s
    web_stats.nine_nine *= ms_p_s

    web_stats.bw = (web_stats.bw / MB_p_B) * bits_p_B

    return web_stats

def write_csv( csv_file, web_stats, main_args, fct_list=None ):
    """ Generate CSV file """
    hdr_fmt = "%s - %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"
    header = hdr_fmt %  ( "Threads",
                          "Connections",
                          "Total Transfer Size (MB)",
                          "Total Requests",
                          "Total Responses",
                          "Total Errors",
                          "Avg. Latency (ms)",
                          "Std. Dev. Latency (%)",
                          "Min. Latency (ms)",
                          "Max. Latency (ms)",
                          "Total Duration (s)",
                          "Bandwidth (Mbps)",
    )
    # mode = "w"
    # if os.path.isfile( csv_file ):
    #     mode = "a"
    # request_enum_header = "thread_num,url_request,req_start,req_finish,fct\n"

    body_fmt = "%s - %s,%.2f,%d,%d,%d,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n"
    next_line = body_fmt % ( main_args.threads,
                             main_args.conns,
                             web_stats.tot_bytes,
                             web_stats.tot_requests,
                             web_stats.tot_responses,
                             web_stats.tot_errors,
                             web_stats.avg_lat,
                             web_stats.stddev_lat,
                             web_stats.min_lat,
                             web_stats.max_lat,
                             web_stats.duration,
                             web_stats.bw,
                           )

    with open( csv_file, 'w+' ) as output_file:
        # to make reading total requests aka througput easier
        output_file.write("P99:\n")
        output_file.write("%s" % str(web_stats.nine_nine)+'\n')
        output_file.write("P90:\n")
        output_file.write("%s" % str(web_stats.nine_zero)+'\n')
        output_file.write('QPS:\n')
        output_file.write("%s" % str(web_stats.tot_responses)+'\n')
        output_file.write('Median Latency:\n')
        output_file.write("%s" % str(web_stats.avg_lat)+'\n')
        output_file.write('95% Tail Latency:\n')
        output_file.write("%s" % str(web_stats.tot_requests)+'\n\n')

        output_file.write('(median for each thread, 95% lat for each thread, lists of fct 90%->100% tail on 20% of results):\n')
        for i in fct_list:
            for j in i:
                output_file.write(str(j)+'\n')
    return
