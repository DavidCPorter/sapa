import os
import sys

elastic_index = '{ "index" : { "_index" : "reviews", "_id" : "%d" }}\n'

with open(sys.argv[1], "r") as f:
    theworld=f.readlines()
try:

    count=1
    indexer=0
    world_len=len(theworld)
    incrementer=int(world_len/10)
    for p in range(10):

        print(p)
        with open("elasticjson%d.json" % p, "w+") as fo:
            for i in theworld[indexer:incrementer]:
                fo.write(elastic_index % count)
                fo.write(i)
                count+=1
            indexer+=incrementer
            incrementer+=incrementer
except e:
    print(e)
