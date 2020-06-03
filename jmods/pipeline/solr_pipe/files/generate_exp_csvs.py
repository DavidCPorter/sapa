import os
import sys
from datetime import datetime
import time
import gzip

def main(args_dict):

    JANUS_HOME=args_dict.get('--proj_home',"/Users/dporter/projects/janus")
    experiment_name=args_dict.get('--exp_name')
    # deploy_name is used to list files in deploy_name dir for the current iteration to be mapped to total.csv
    deploy_name=args_dict.get('--deploy_name')
    exp_home = JANUS_HOME + "/data_dir/"+experiment_name
    totals_dir = exp_home
    total_scale_file = totals_dir + '/total_' + experiment_name + '.csv'

    query=args_dict.get('--query')
    engine=args_dict.get('--engine')
    csize=args_dict.get('--clustersize')
    replicas=args_dict.get('--replicas')
    shards=args_dict.get('--shards')

    def main_inner():
        nonlocal JANUS_HOME,experiment_name,deploy_name,exp_home,totals_dir,total_scale_file,query,engine,csize,replicas,shards
        print('******** FINISHED FULL SCALING EXPERIEMENT **********')
        print("\n\nRUNNING generate_exp_csvs.py ")
        QPS = []
        median_lat = []
        tail_lat = []
        dirs = os.popen('ls '+exp_home+' | grep '+deploy_name).read()
        dirs = dirs.split('\n')
        dirs.pop()
        try:
            os.makedirs(totals_dir)
        except FileExistsError:
            print("file exists\n\n\n")
         # directory already exists
            pass

    # this is for total file
        fm = open(total_scale_file, "a+")
        fm.write('engine,parallel_requests,QPS,P50_latency(ms),P90_latency(ms),P95_latency(ms),P99_latency(ms),clustersize,query,rfshards,GROUP,fcts,\n')

        for d in dirs:
            print(d)
            bench_files = os.popen('ls '+exp_home+'/'+d ).read()
            print("these are the output files for "+d+" janus experiment")
            print(bench_files)
            bench_files = bench_files.split('\n')
            bench_files.pop()
            # since i added engine prefix need to remove it
            for exp_output in bench_files:
                f = open(exp_home+'/'+d+'/'+exp_output, 'r')
                data = f.readline()
                print("data = ", data)
                data=data.replace("\n","")
                fcts= f.readline()
                print(fcts)
                fct_data=fcts.strip()
                fct_data=fct_data.replace(" ",'')
                fct_data=fct_data.replace("[",'')
                fct_data=fct_data.replace("]",'')
                fct_data=fct_data.replace("\n",'')
                fct_string=fct_data.replace(",","--")
                f.close()

                if csize == "0":
                    csize = "1"

                fm = open(total_scale_file, "a+")
                fm.write(engine+','+data+','+csize+','+query+','+replicas+'_'+shards+','+deploy_name+','+fct_string+'\n')
                fm.close()

        print("\n COMPLETED generate_exp_csvs.py \n\n\n")
        return

    return main_inner


if __name__ == "__main__":
    args = sys.argv[1:]
    arg_dict = {args[x]: args[x + 1] for x in range(0, len(args) - 1) if x % 2 == 0}
    inner = main(arg_dict)
    inner()

    sys.exit()
