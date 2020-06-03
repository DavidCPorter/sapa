#!/bin/bash
curl -X POST -H 'Content-type: application/json' -d '{"add-directoryfactory": {"class": "org.apache.solr.core.RAMDirectoryFactory" }}' http://$1:8983/solr/${2}/config
