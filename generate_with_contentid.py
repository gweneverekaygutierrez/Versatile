import random

MAX_NODE_ID = 100 
MAX_CONTENT_ID = 1000
MAX_COUNTENT_ID_COUNT = 50
MIN_CPU = 10
MAX_CPU = 50
MIN_BANDWIDTH = 10
MAX_BANDWIDTH = 50

SN_CPU = 0
SN_BW = 1
SN_CID = 2

substrate_network = {}
for nodeid in range(MAX_NODE_ID):
  cpu = random.randint(MIN_CPU, MAX_CPU)
  bw = random.randint(MIN_BANDWIDTH, MAX_BANDWIDTH)
  cid_count = random.randint(1, MAX_COUNTENT_ID_COUNT)
  cid = random.sample(range(MAX_CONTENT_ID), cid_count)
  substrate_network[nodeid] = [cpu, bw, cid]

file_sn = open("substrate_network.txt", "w")
file_vnr = open("virtual_network_requests.txt", "w")

id_str, cpu_str, bw_str = "", "", ""
for nodeid, info in substrate_network.items():
  id_str = id_str + str(nodeid) + " "
  cpu_str = cpu_str + str(info[SN_CPU]) + " "
  bw_str = bw_str + str(info[SN_BW]) + " "

file_sn.write(id_str.strip() + "\n")
file_sn.write(cpu_str.strip() + "\n")
file_sn.write(bw_str.strip() + "\n\n")

for nodeid, info in substrate_network.items():
  file_sn.write(" ".join(map(str, info[SN_CID])) + "\n")
  





