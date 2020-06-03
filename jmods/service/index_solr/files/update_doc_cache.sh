#!/bin/bash

curl -X POST -H 'Content-type: application/json' -d '{"set-property": {"query.queryResultMaxDocsCached": 1800000, "query.documentCache.size": 1800000, "query.documentCache.initialSize": 1800000 , "query.documentCache.autowarmCount" : 1800000 }}' http://$1:8983/solr/${2}/config
