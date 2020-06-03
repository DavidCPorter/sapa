#!/bin/bash

curl http://$1:8983/solr/${2}/schema -X POST -H 'Content-type:application/json' --data-binary '{
    "add-field" : {
        "name":"reviewerID",
        "type":"text_general",
        "multiValued":false,
        "stored":true
    },
    "add-field" : {
        "name":"asin",
        "type":"string",
        "multiValued":true,
        "stored":true
    },
    "add-field" : {
        "name":"reviewerName",
        "type":"string",
        "multiValued":true,
        "stored":true
    },
    "add-field" : {
        "name":"reviewText",
        "type":"text_general",
        "stored":true
    },
    "add-field" : {
        "name":"overall",
        "type":"string",
        "multiValued":true,
        "stored":true
    },
    "add-field" : {
        "name":"summary",
        "type":"text_general",
        "multiValued":true,
        "stored":true
    }
}'
