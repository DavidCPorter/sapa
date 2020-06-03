#!/bin/bash

{% for connection in range(procs | int) %}
python3 traffic_gen.py --threads 1 --duration {{load_duration}} --replicas {{replicas}} --shards {{shards}} --query {{query}} --loop {{loop_type}} --solrnum {{solrnum}}  --engine {{engine}} --connections 1 --output-dir ./ --host {{endpoint_host}}{{connection%solrnum+1}} --port {{endpoint_port}} >/dev/null 2>&1 &
{% endfor %}
python3 traffic_gen.py --threads 1 --duration {{load_duration}} --replicas {{replicas}} --shards {{shards}} --query {{query}} --loop {{loop_type}} --solrnum {{solrnum}}  --engine {{engine}} --connections 1 --output-dir ./ --host {{endpoint_host}}2 --port {{endpoint_port}}
sleep 3


