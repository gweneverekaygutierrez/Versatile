import random

output_file_1 = open('topology.txt', 'w')

cpu_resources = [] 
for cpu_index in range(10):
	cpu_resources.append(2000)

for cpu_index in range(len(cpu_resources)):
	if cpu_index == len(cpu_resources) - 1:
		output_file_1.write(str(cpu_resources[cpu_index]) + "\n")
	else:
		output_file_1.write(str(cpu_resources[cpu_index]) + " ")

bw_resources = []
for bw_index1 in range(10):
	bw_resources.append([])
	for bw_index2 in range(10):
		bw_resources[bw_index1].append(2000)

for bw_index1 in range(len(bw_resources)):
	for bw_index2 in range(len(bw_resources[0])):
		if bw_index1 == bw_index2:
			bw_resources[bw_index1][bw_index2] = 0
		if bw_index2 == len(bw_resources[0]) - 1: 
			output_file_1.write(str(bw_resources[bw_index1][bw_index2]) + "\n")
		else:
			output_file_1.write(str(bw_resources[bw_index1][bw_index2]) + " ")

output_file_2 = open('requests.txt', 'w')

for vnr_id in range(1,1001):
	output_file_2.write(str(vnr_id) + "\n")
	cpu_resources = random.sample(range(10,21), 3)
	bw_resources = [random.sample(range(10,21), 3) for i in range(3)]
	
	for cpu_index in range(len(cpu_resources)):
		if cpu_index == len(cpu_resources) - 1:
			output_file_2.write(str(cpu_resources[cpu_index]) + "\n")
		else:
			output_file_2.write(str(cpu_resources[cpu_index]) + " ")
	
	for bw_index1 in range(len(bw_resources)):
		for bw_index2 in range(len(bw_resources[0])):
			if bw_index1 == bw_index2:
				bw_resources[bw_index1][bw_index2] = 0
			if bw_index2 == len(bw_resources[0]) - 1: 
				output_file_2.write(str(bw_resources[bw_index1][bw_index2]) + "\n")
			else:
				output_file_2.write(str(bw_resources[bw_index1][bw_index2]) + " ")

	if vnr_id < 1000:
		output_file_2.write(str("\n"))