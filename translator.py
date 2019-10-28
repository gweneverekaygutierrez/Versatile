import numpy as np
import re


# Topology head transfer
with open('test1.txt') as f:
    list = [x.split() for x in f]

file = open("test1.txt")
file_new = open("T_first.txt", "w")

for x in range(len(list[0])):
    for y in range(len(list)):
        file_new.write(list[y][x] + " ")
    file_new.write("\n")

file.close()
file_new.close()

# Protocol translate
fp3 = open("Neighbor.txt", "r")
fp4 = open("T_second.txt", "w")

for s in fp3.readlines():
    fp4.write(s.replace("BLE", "1").replace("WIFI", "2"))

fp3.close()
fp4.close()

# topology made
file2 = open("T_first.txt")

lines = file2.readlines()
node = lines[0]

nx = ny = int(max(node))
topology_1 = np.zeros((ny, nx))   # BLE
topology_2 = np.zeros((ny, nx))   # WIFI


ff = open('test1.txt', "r")
lines = ff.readlines()
result = []
for x in lines:
    a = result.append(x.split(' ')[0])
    print(a)

ff.close()

for i in a:
    for j in b:
        for h in bw:
            topology_1[i][j] = bw[h]
            topology_1[j][i] = bw[h]


file2.close()
#file3.close()



'''
filepath = "test1.txt"
filepath_neighbor_id = "N_id.txt"
filepath_protocol = "Protocol.txt"
filepath_bw = "bandwidth.txt"

file = open(filepath)

file_new1 = open(filepath_neighbor_id, "w")
file_new2 = open(filepath_protocol, "w")
file_new3 = open(filepath_bw, "w")
for line in file:
    arr = line.split(';')
    file_new1.write(arr[0] + "\n")
    file_new2.write(arr[1] + "\n")
    file_new3.write(arr[2])

file.close()
file_new1.close()
file_new2.close()
file_new3.close()

# Topology Translate
with open('N_id.txt') as input_file:
    read_data = input_file.read()
neighbor = []
node = []
for line in read_data.split("\n")[:-1]:
    neighbor.append([int(data) for data in line.split()])
for i in read_data.split():
    node.append(i)
#print(node)

with open('bandwidth.txt') as input_file:
    read_data = input_file.read()
bws = []
for i in read_data.split():
    bws.append(i)

neighbor_list = np.mat(neighbor)
print(neighbor_list)

maxid = node
BW = [int(i) for i in bws]
print(BW)
nx = ny = int(max(maxid))

topology = np.zeros((ny, nx))
print(topology)

for y, x in ((y, x) for y in range(ny) for x in range(nx)):
    for i in BW:
        topology[y, x] = i
print(topology)
'''
