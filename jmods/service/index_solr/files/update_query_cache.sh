#!/bin/bash

curl -X POST -H 'Content-type: application/json' -d '{"set-property": {"query.queryResultCache.size": 1000000, "query.queryResultCache.initialSize": 1000000 , "query.queryResultCache.autowarmCount": 1000000 }}' http://$1:8983/solr/${2}/config
