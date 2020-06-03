#!/bin/bash
export JANUS_HOME=/Users/dporter/projects/janus
CL_USER=dporte7
CHECKSOLRARGS='ps aux | grep solr'
CHECKPORTSARGS='lsof -i | grep LISTEN'
KILLARGS="ps aux | grep -i solrclientserver | awk -F' ' '{print \$2}' | xargs kill -9"
CHECKARGS='ps aux | grep -i solrcloud_loadbalancer'
alias utilsview="cat $JANUS_HOME/utils/utils.sh"
alias grepmal="cd $JANUS_HOME/; pssh -l $CL_USER -h ssh_files/pssh_solr_node_file -P 'ps aux | grep kdevtmpfsi > tmpout.txt;head -n 1 tmpout.txt'"
alias whatsgood="cd $JANUS_HOME/benchmark_scripts/profiling_data/exp_results; ls -t; cat * */*;cd $JANUS_HOME"
alias mechart="python3 $JANUS_HOME/chart/chartit_error_bars.py"
alias killallbyname="cd /Users/dporter/projects/solrcloud;pssh -i -h ssh_files/pssh_all -l dporte7 -P sudo pkill -f"
alias fullog="cd $JANUS_HOME/; pssh -l $CL_USER -h ssh_files/pssh_solr_node_file -P 'tail -n 100 /var/solr/logs/solr.log | grep ERROR'"
alias grepnodeprocs="cd $JANUS_HOME/; pssh -l $CL_USER -h ssh_files/pssh_solr_node_file -P 'ps aux | grep'"
alias callingnodes="cd $JANUS_HOME/; pssh -l $CL_USER -h ssh_files/pssh_all -P"
alias wipetraffic="cd $JANUS_HOME;pssh -l $CL_USER -h ssh_files/pssh_traffic_node_file 'echo hey >traffic_gen/traffic_gen.log'"
alias viewtraffic="cd $JANUS_HOME;pssh -l $CL_USER -h ssh_files/pssh_traffic_node_file -P 'tail -n 2000 traffic_gen/traffic_gen.log'"
alias viewsolrj="cd $JANUS_HOME;pssh -l $CL_USER -h ssh_files/pssh_traffic_node_file -P 'tail -n 2000 solrclientserver/solrjoutput.txt'"
alias play="cd $JANUS_HOME/playbooks; ansible-playbook -i ../inventory"
alias solo_party="cd $JANUS_HOME/playbooks; ansible-playbook -i ../inventory_local"
alias killsolrj='cd $JANUS_HOME;pssh -i -h ssh_files/pssh_traffic_node_file -l $CL_USER $KILLARGS'
alias clearout="cd $JANUS_HOME/benchmark_scripts; echo ''> nohup.out"
alias viewout="cd $JANUS_HOME/benchmark_scripts; tail -n 1000 nohup.out"
alias checksolrj="cd $JANUS_HOME;pssh -i -h ssh_files/pssh_traffic_node_file -l $CL_USER $CHECKARGS"
alias checksolr="cd $JANUS_HOME;pssh -i -h ssh_files/pssh_solr_node_file -l $CL_USER $CHECKSOLRARGS"
alias checkports="cd $JANUS_HOME;pssh -i -h ssh_files/solr_single_node -l $CL_USER $CHECKPORTSARGS"
alias checkcpu="cd $JANUS_HOME/; pssh -l $CL_USER -h ssh_files/pssh_all -P 'top -bn1 > cpu.txt;head -10 cpu.txt | grep dporte7'"
# alias delete_collections="python3 $JANUS_HOME/utils/delete_collection.py"
alias singlelogs="cd $JANUS_HOME/; pssh -l $CL_USER -h ssh_files/solr_single_node -P 'tail -n 1000 /var/solr/logs/solr.log'"

# alias archive_fcts="cd $JANUS_HOME/benchmark_scripts;cp -rf *.zip ~/exp_results_fct_zips/$(date '+%Y-%m-%d_%H:%M');rm -rf *.zip"
alias singletest="cd $JANUS_HOME/benchmark_scripts; bash exp_scale_loop_single.sh"
alias fulltest="cd $JANUS_HOME/benchmark_scripts; bash exp_scale_loop.sh"
alias dockertest="cd $JANUS_HOME/benchmark_scripts; bash exp_scale_loop_docker.sh"
alias listcores="cd $JANUS_HOME/; pssh -l $CL_USER -i -h ssh_files/pssh_solr_node_file 'ls /users/$CL_USER/solr-8_3/solr/server/solr'"
alias deldown="cd $JANUS_HOME/; pssh -l $CL_USER -i -h ssh_files/solr_single_node 'bash ~/solr-8_3/solr/bin/solr delete -c'"
alias checkdisk="cd $JANUS_HOME/; pssh -h ssh_files/pssh_solr_node_file -l $CL_USER -P 'df | grep /dev/nvme0n1p1'"

alias checkconfig="cd $JANUS_HOME/; pssh -l $CL_USER -i -h ssh_files/solr_single_node 'cat ~/solr-8_3/solr/server/solr/configsets/_default/conf/solrconfig.xml'"
alias collectionconfig="curl http://128.110.153.162:8983/solr/reviews_rf4_s1_clustersize94/config"
alias collectionconfigfull="curl http://128.110.153.162:8983/solr/reviews_rf32_s1_clustersize16/config"
alias daparams="vim $JANUS_HOME/benchmark_scripts/utils/exp_scale_loop_params.sh"
alias davars="vim $JANUS_HOME/playbooks/janus_vars.yml"

export CORE_HOME=/users/dporte7/solr-8_3/solr/server/solr


export node0="128.110.154.10"
export node1="128.110.154.24"
export node2="128.110.154.27"
export node3="128.110.154.21"
export node4="128.110.153.252"
export node5="128.110.154.20"
export node6="128.110.154.13"
export node7="128.110.153.246"
export node8="128.110.153.244"
export node9="128.110.154.4"
export node10="128.110.154.31"
export node11="128.110.154.7"
export node12="128.110.154.25"
export node13="128.110.154.35"
export node14="128.110.154.18"
export node15="128.110.153.245"
export node16="128.110.154.11"
export node17="128.110.154.16"
export node18="128.110.154.26"
export node19="128.110.154.15"
export node20="128.110.154.12"
export node21="128.110.153.253"
export node22="128.110.154.17"
export node23="128.110.154.9"

# # cannot export ARRAYS in bash : ) so we do this instead
export ALL_NODES=" $node0 $node1 $node2 $node3 $node4 $node5 $node6 $node7 $node8 $node9 $node10 $node11 $node12 $node13 $node14 $node15 $node16 $node17 $node18 $node19 $node20 $node21 $node22 $node23 "
export ALL_SOLR=" $node0 $node1 $node2 $node3 $node4 $node5 $node6 $node7 $node8 $node9 $node10 $node11 $node12 $node13 $node14 $node15 "
export ALL_LOAD=" $node16 $node17 $node18 $node19 $node20 $node21 $node22 $node23 "
alias ssher="ssh -l $CL_USER"
#source $JANUS_HOME/benchmark_scripts/utils/exp_helpers.sh
shopt -s expand_aliases

