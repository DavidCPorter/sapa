#!/bin/bash
source ${JANUS_HOME}/benchmark_scripts/utils/utils.sh

cd $JANUS_HOME/utils/ssh_files
count=0
ips=()
for n in $ALL_LOAD;do
  echo $n
	count=$(($count+1))
	ips+=("$n")
	rm pssh_traffic_node_file_$count
	touch pssh_traffic_node_file_$count
	for i in "${ips[@]}";do
		echo $i >> pssh_traffic_node_file_$count
	done
done
rm pssh_traffic_node_file
touch pssh_traffic_node_file
for i in $ALL_LOAD;do
	echo $i >> pssh_traffic_node_file
done

rm pssh_solr_node_file
touch pssh_solr_node_file
for n in $ALL_SOLR;do
	echo $n >> pssh_solr_node_file
done

rm pssh_zoo_node_file
touch pssh_zoo_node_file
count=1
for n in $ALL_SOLR;do
	echo $n >> pssh_zoo_node_file
	if [ $count -eq 3 ];then
		break
	fi
	count=$(($count+1))
done

rm pssh_all
touch pssh_all
for n in $ALL_NODES;do
	echo $n >> pssh_all
done

rm solr_single_node
touch solr_single_node
echo $node0 >> solr_single_node
