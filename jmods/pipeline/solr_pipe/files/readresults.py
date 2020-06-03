import os
import sys
from datetime import datetime
import time
import gzip
import pdb


# args = $THREADS $DURATION $CON $QUERY $LOOP $PROCESSES

# def main(p, t, d, rf, q, l, shards, solrnum, loadnodes, instances=None, engine=''):
# decided to use a closure here in lieu of doing this in primary function... primary function originally had these variable names
def main(args_dict):
    p = args_dict['--processes']
    t= args_dict['--threads']
    d= args_dict['--duration']
    rf= args_dict['--replicas']
    q= args_dict['--query']
    l= args_dict['--loop']
    shards= args_dict['--shards']
    solrnum= args_dict['--solrnum']
    instances= args_dict['--instances']
    engine= args_dict['--engine']
    csv_location = args_dict['--csv_location']
    result_filename = args_dict['--result_filename']

    def main_inner():
        nonlocal p,t,d,rf,q,l,shards,solrnum,instances,engine,csv_location
        print('\n\nRUNNING readresults.py ::: ARGS == proc=%s threads=%s duration=%s' % (p, t, d))
        QPS = []
        median_lat = []
        tail_lat = []
        ninenine = []
        ninezero = []
        fct_total_string = ''
        files = os.popen('ls ' + csv_location + '| grep csv').read()
        files = files.split('\n')
        processes = float(len(files))
        print("num output files copied from remote == %s | should == %s (num procs passsed in to this script)" % (
        str(processes * int(t)), p))
        files.pop()
        for file in files:
            f = open(csv_location + "/" + file, 'r')
            #
            result_page = f.readlines()
            # read first line which is the request total
            ninenine.append(result_page[1])
            ninezero.append(result_page[3])
            QPS.append(result_page[5])
            median_lat.append(result_page[7])
            tail_lat.append(result_page[9])
            fct_total_string = fct_total_string + "," + str(result_page[17])

            f.close()

        sum_queries_per_second = 0.0
        for i in QPS:
            sum_queries_per_second += float(i)

        sum_median_lat = 0
        for i in median_lat:
            sum_median_lat += float(i)

        sum_tail_lat = 0
        for i in tail_lat:
            sum_tail_lat += float(i)

        sum_ninenine_lat = 0
        for i in ninenine:
            sum_ninenine_lat += float(i)

        sum_ninezero_lat = 0
        for i in ninezero:
            sum_ninezero_lat += float(i)

        # fct_total_string=fct_total_string.replace(' ','')
        fct_total_string = fct_total_string.replace('\n', '')
        fct_total_string = fct_total_string.replace('[', '')
        fct_total_string = fct_total_string.replace(']', '')
        fct_total_string = fct_total_string.replace(' ', '')

        fct_total_list = fct_total_string.split(",")
        fct_total_list = [float(i) for i in fct_total_list[1:]]

        total_qps = round(sum_queries_per_second, 2)
        total_med_lat = float(sum_median_lat / float(processes))
        total_tail_lat = float(sum_tail_lat / float(processes))
        total_ninenine_lat = float(sum_ninenine_lat / float(processes))
        total_ninezero_lat = float(sum_ninezero_lat / float(processes))

        fct_total_list.sort()
        fct_len = len(fct_total_list)
        incrementer_95 = int(fct_len / 20)
        # incrementer_50=int(fct_len/2)
        # incrementer_90=int(fct_len/10)
        # incrementer_99=int(fct_len/100)
        # gonna make a list [0,5,10,... 100] and save to text file and that will be the data read into the CDF chart

        p_95 = [fct_total_list[incrementer_95 * x] for x in range(0, 20)]
        # p_95=[fct_total_list[incrementer*x] for x in range(0,20)]
        # fct_percentiles_95=[fct_total_list[incrementer*x] for x in range(0,20)]
        # fct_percentiles_95=[fct_total_list[incrementer*x] for x in range(0,20)]

        # denote this is a single node cluster record if not default 0.
        if instances != "0":
            print("SINGLE NODE READRESULTS ")
            solrnum = '9' + str(solrnum)


        iter_result_path = csv_location+'/readresults_dir'

        try:
            os.makedirs(iter_result_path)
        except FileExistsError:
            print("file exists\n\n\n")
            # directory already exists
            pass

        fp = open(
                iter_result_path + '/' + result_filename, 'w+'
        )


        fp.write(p + ',' + str(total_qps) + ',' + str(total_med_lat) + ',' + str(total_ninezero_lat) + "," + str(
            total_tail_lat) + "," + str(total_ninenine_lat) + '\n')
        fp.write(str(p_95))
        # fp.write(str(p_90))
        # fp.write(str(p_50))
        # fp.write(str(p_99))

        fp.close()


        print("READRESULTS SCRIPT COMPLETE\n\n\n")
        return

    return main_inner


if __name__ == "__main__":


    args = sys.argv[1:]
    arg_dict = {args[x]: args[x + 1] for x in range(0, len(args) - 1) if x % 2 == 0}

    inner = main(arg_dict)
    inner()

    sys.exit()
