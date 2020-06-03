import sys
import time
import subprocess
import copy



def getAdHocDict():
    d = dict()
    d['test'] = "--hosts solr1,solr2 -vars example_variables.yml --inv /Users/dporter/projects/janus/inv_special --tags activate --path experiments/main.yml"
    d['copyscripts'] = "--hosts generatorNode --play copy_scripts.yml --vars example_variables.yml --module http_closed_loop --inv /Users/dporter/projects/janus/local_var_inventory --tags activate --stage load"
    d['runscripts']  = "--hosts generatorNode --play run.yml --vars example_variables.yml --module http_closed_loop --inv /Users/dporter/projects/janus/local_var_inventory --tags activate --stage load"
    d['mkdatadir']  = "--hosts localhost --play mkdir_data_local.yml --vars example_variables.yml --module solr_pipe --inv /Users/dporter/projects/janus/local_var_inventory --tags activate --stage pipeline"
    d['readresults']  = "--hosts generatorNode --play read_results.yml --vars example_variables.yml --module solr_pipe --inv /Users/dporter/projects/janus/local_var_inventory --tags activate --stage pipeline"
    d['appendresults']  = "--hosts localhost --play append_results_to_total.yml --vars example_variables.yml --module solr_pipe --inv /Users/dporter/projects/janus/local_var_inventory --tags activate --stage pipeline"
    d['cdf']  = "--hosts localhost --play generate_cdf.yml --vars example_variables.yml --module cdf --inv /Users/dporter/projects/janus/local_var_inventory --tags activate --stage viz"
    return d

def getDfsDict():
    default_vars = "example_variables.yml"
    example_of_branch_vars = "example_vars.yml"
    DFS_dict = {
        "stage": "env",
        "module": "cloud-env",
        "hosts": "all:!mylocal",
        "play": "install_tasks.yml",
        "vars": default_vars,
        "next": {
            "stage": "env",
            "module": "cloud-env",
            "hosts": "all:!mylocal",
            "play": "aws_tasks.yml",
            "vars": default_vars,
            "next": {
                "stage": "service",
                "module": "zookeeper",
                "hosts": "zookeeperNodes",
                "play": "download_tasks.yml",
                "vars": default_vars,
                "next": {
                    "stage": "service",
                    "module": "zookeeper",
                    "hosts": "zookeeperNodes",
                    "play": "configure_tasks.yml",
                    "vars": default_vars,
                    "next": {
                        "stage": "service",
                        "module": "zookeeper",
                        "hosts": "zookeeperNodes",
                        "play": "run_tasks.yml",
                        "vars": default_vars,
                        "next": {
                            "stage": "service",
                            "module": "solr",
                            "hosts": "twoNode",
                            "play": "install_tasks.yml",
                            "vars": default_vars,
                            "next": {
                                "stage": "service",
                                "module": "solr",
                                "hosts": "twoNode",
                                "play": "config_tasks.yml",
                                "vars": default_vars,
                                "next": {
                                    "stage": "service",
                                    "module": "solr",
                                    "hosts": "twoNode",
                                    "play": "run_tasks.yml",
                                    "vars": default_vars,
                                    "next": {
                                        "stage": "service",
                                        "module": "amazon-reviews-large",
                                        "hosts": "singleNode",
                                        "play": "download_json.yml",
                                        "vars": default_vars,
                                        "next": {
                                            "stage": "service",
                                            "module": "index_solr",
                                            "hosts": "twoNode",
                                            "play": "0_pre_index_config.yml",
                                            "vars": default_vars,
                                            "next": {
                                                "stage": "service",
                                                "module": "index_solr",
                                                "hosts": "singleNode",
                                                "play": "1_index.yml",
                                                "vars": default_vars,
                                                "next": {
                                                    "stage": "service",
                                                    "module": "index_solr",
                                                    "hosts": "singleNode",
                                                    "play": "3_post_index_config.yml",
                                                    "vars": default_vars,
                                                    "next": {
                                                    },
                                                    "branches": []
                                                },
                                                "branches": []
                                            },
                                            "branches": []
                                        },
                                        "branches": []
                                    },
                                    "branches": []
                                },
                                "branches": []
                            },
                            "branches": []
                        },
                        "branches": []
                    },
                    "branches": []
                },
                "branches": []
            },
            "branches": [{
                # "module": "zookeeper",
                # "hosts": "zookeeperNodes",
                # "play": "download_tasks.yml",
                # "vars": example_of_branch_vars,
                # "next": {
                #     "module": "zookeeper",
                #     "hosts": "zookeeperNodes",
                #     "play": "download_tasks.yml",
                #     "vars": default_vars,
                #     "next": {},
                #     "branches": []
                # },
                # "branches": []
            }]
        },
        "branches": []
    }

    print(DFS_dict)
    return DFS_dict