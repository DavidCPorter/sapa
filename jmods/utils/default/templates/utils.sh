#!/bin/bash
export JANUS_HOME={{JANUS_HOME}}
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


{% for host in groups['allNodes'] %}
export node{{loop.index-1}}="{{host}}"
{% endfor %}

# # cannot export ARRAYS in bash : ) so we do this instead
export ALL_NODES="{% for host in groups['allNodes'] %} $node{{loop.index-1}}{%- if loop.last %} "{% endif %}
{% endfor %}

export ALL_SOLR="{% for host in groups[searchGroupArg] %} $node{{loop.index-1}}{%- if loop.last %} "{% endif %}
{% endfor %}

export ALL_LOAD="{% for host in groups['generatorNode'] %} $node{{loop.index+searchnodecount-1}}{%- if loop.last %} "{% endif %}
{% endfor %}

alias ssher="ssh -l $CL_USER"
#source $JANUS_HOME/benchmark_scripts/utils/exp_helpers.sh
shopt -s expand_aliases

