import sys
import os

node_block = []
file = open("profile_node.xml", 'r')
line = file.readline()
while line:
    node_block.append(line)
    line= file.readline()

file.close()

open("profile_output.xml", 'w+')

header = '<rspec xmlns="http://www.geni.net/resources/rspec/3" xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" xmlns:tour="http://www.protogeni.net/resources/rspec/ext/apt-tour/1" xmlns:jacks="http://www.protogeni.net/resources/rspec/ext/jacks/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.geni.net/resources/rspec/3    http://www.geni.net/resources/rspec/3/request.xsd" type="request">\n'

node = '<node xmlns="http://www.geni.net/resources/rspec/3" client_id="node-%d">\n'

node_interface = '<interface xmlns="http://www.geni.net/resources/rspec/3" client_id="interface-%d"/>\n'

link = '<link xmlns="http://www.geni.net/resources/rspec/3" client_id="link-0"><link_type xmlns="http://www.geni.net/resources/rspec/3" name="lan"/>\n'

interface_ref = '<interface_ref xmlns="http://www.geni.net/resources/rspec/3" client_id="interface-%d"/>\n'

property = '<property xmlns="http://www.geni.net/resources/rspec/3" source_id="interface-%d" dest_id="interface-%d" />\n'


footer =  '<site xmlns="http://www.protogeni.net/resources/rspec/ext/jacks/1" id="undefined"/>\n</link>\n</rspec>'

disk = '<emulab:blockstore name="bs%d" mountpoint="/mydata" class="local" size="50GB" placement="any"/>\n'

# write Node definitions

output = open("profile_output.xml", 'a+')
node_num = 0
output.write(header)
for i in range(0,int(sys.argv[1])):
    line_num = 0
    for j in node_block:
        if line_num == 0:
            output.write(node % node_num)
        elif line_num == 6:
            output.write(node_interface % node_num)
        elif line_num == 7:
            output.write(disk % node_num)
        else:
            output.write(j)

        line_num+=1
    node_num+=1

#  write LAN part
output.write(link)
node_num = 0
for i in range(0,int(sys.argv[1])):
    output.write(interface_ref % node_num)
    node_num+=1

for i in range(0,int(sys.argv[1])):
    for j in range(0,int(sys.argv[1])):
        if j == i:
            continue
        output.write(property % (i,j))

output.write(footer)
