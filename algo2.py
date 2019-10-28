import networkx as nx 
import matplotlib.pyplot as plt 
import string
from collections import deque
import pulp

def GenerateNodes(network, node_attributes):
	for node_index in range(len(node_attributes)):
		network.add_node(alphabet_dict[node_index+1], cpu=node_attributes[node_index])


def GenerateEdges(network, edge_attributes):
	for row in range(len(edge_attributes)):
		for column in range(len(edge_attributes[0])):
			if edge_attributes[row][column] > 0:
				network.add_edge(alphabet_dict[row+1], alphabet_dict[column+1], bw=edge_attributes[row][column])


def GetRevenue(vnr_list):
	for vnr_index in range(len(vnr_list)):
		revenue_components = []
		for node in vnr_list[vnr_index].nodes():
			revenue_components.append(vnr_list[vnr_index].nodes[node]['cpu'])
		for edge in vnr_list[vnr_index].edges():
			revenue_components.append(vnr_list[vnr_index].edges[edge]['bw'])
		vnr_list[vnr_index] = (vnr_list[vnr_index], sum(revenue_components))

	vnr_list.sort(key=lambda x:x[1], reverse=True)

'''
def GetMaximumCPU(vnr):
	maximum_cpu = 0
	for node in vnr.nodes():
		if vnr.nodes[node]['cpu'] > maximum_cpu:
			maximum_cpu = vnr.nodes[node]['cpu']

	return maximum_cpu

def GetMaximumBW(vnr):
	maximum_bw = 0
	for edge in vnr.edges():
		if vnr.edges[edge]['bw'] > maximum_bw:
			maximum_bw = vnr.edges[edge]['bw']

	return maximum_bw
'''


def GetAvailableNodes(sn, maximum_cpu):
	possible_sn_nodes = []
	for node in sn.nodes():
		if sn.nodes[node]['cpu'] >= maximum_cpu:
			possible_sn_nodes.append(node)

	return possible_sn_nodes


def GetMaxAvailableResources(sn, sn_subset):
	for node_index in range(len(sn_subset)):
		max_available_resources = 0
		for edge in sn.edges(sn_subset[node_index]):
			max_available_resources += sn.edges[edge]['bw']

		max_available_resources *= sn.nodes[sn_subset[node_index]]['cpu']
		sn_subset[node_index] = (sn_subset[node_index], max_available_resources)

	sn_subset.sort(key=lambda x:x[1], reverse=True)


def SortVnrNodes(vnr):
	cpu = []
	for node in vnr.nodes():
		cpu.append(vnr.nodes[node]['cpu'])

	if cpu[1:] == cpu[:-1]:
		return sorted(vnr.nodes(data=True))
	else:
		return sorted(vnr.nodes(data=True), key=lambda x: x[1]['cpu'], reverse=True)


def AddNodeMapping(node_mapping_list, vnr_id, vnr_node, sn_node):
	node_mapping_list.append((vnr_id, vnr_node, sn_node))


def SubtractCpuResource(sn, sn_node, vnr, vnr_node):
	sn.nodes[sn_node]['cpu'] -= vnr.nodes[vnr_node]['cpu']


def GreedyNodeMapping(sn, vnr_list, node_mapping_list, request_queue):
	successful_node_mapping = []
	for vnr in vnr_list:
		maximum_cpu = max(vnr[0].nodes(data=True), key=lambda x: x[1]['cpu'])[1]['cpu']
		possible_sn_nodes = GetAvailableNodes(sn, maximum_cpu)

		GetMaxAvailableResources(sn, possible_sn_nodes)
		if vnr[0].number_of_nodes() > len(possible_sn_nodes):
			request_queue.append(vnr[0])
			continue

		else:
			vnr[0].graph['node_mapping_status'] = 1
			#print("POSSIBLE NODES: ", possible_sn_nodes)
			#print("SN NODES: ", sorted(sn.nodes().data()))
			sorted_vnr_nodes = SortVnrNodes(vnr[0])
			#print("VNR NODES: ", sorted_vnr_nodes)
			#print("")
			for node in sorted_vnr_nodes:
				#print("NODE:", node)
				selected_sn_node = possible_sn_nodes.pop(0)
				#print("SELECTED NODE:", selected_sn_node)
				AddNodeMapping(node_mapping_list, vnr[0].graph['id'], node[0], selected_sn_node[0])
				SubtractCpuResource(sn, selected_sn_node[0], vnr[0], node[0])
				#print("SN NODES DATA:", sorted(sn.nodes.data()))
				#print("")

		if vnr[0].graph['node_mapping_status'] == 1:
			successful_node_mapping.append(vnr[0])

	#print(node_mapping_list)
	#print("")
	return(successful_node_mapping)


def AddEdgeMapping(edge_mapping_list, vnr_id, vnr_edge, sn_path):
	edge_mapping_list.append((vnr_id, vnr_edge, sn_path))


def SubtractCpuResource(sn, sn_node, vnr, vnr_node):
	sn.nodes[sn_node]['cpu'] -= vnr.nodes[vnr_node]['cpu']


def SubtractBwResource(sn, sn_edge, vnr, vnr_edge):
	sn.edges[sn_edge]['bw'] -= vnr.edges[vnr_edge]['bw']


def GetSnNodeMapping(node_mapping_list, vnr_id, vnr_node):
	with_vnr_id = list(filter(lambda x: x[0] == vnr_id, node_mapping_list))
	with_node = list(filter(lambda x: x[1] == vnr_node, with_vnr_id))

	return with_node[0][2]


def UnsplittableLinkMapping(sn, vnr_list, node_mapping_list, edge_mapping_list, request_queue):
	for vnr in vnr_list:
		#print("VNR ID: ", vnr[0].graph['id'])
		selected_paths = []
		for edge in sorted(vnr[0].edges()):
			node1 = GetSnNodeMapping(node_mapping_list, vnr[0].graph['id'], edge[0])
			node2 = GetSnNodeMapping(node_mapping_list, vnr[0].graph['id'], edge[1])
			for path in list(nx.shortest_simple_paths(sn, node1, node2)):
				to_map = 1
				for edge_index in range(len(path)-1):
					if vnr[0].edges[edge]['bw'] > sn.edges[path[edge_index], path[edge_index+1]]['bw']:
						to_map = -1
						break
				if to_map == 1:
					selected_paths.append(path)
					break

		if (len(selected_paths) < vnr[0].number_of_edges()):
			request_queue.append(vnr[0])
			continue
		else: 
			vnr[0].graph['edge_mapping_status'] = 1
			for edge in sorted(vnr[0].edges()):
				path = selected_paths.pop(0)
				AddEdgeMapping(edge_mapping_list, vnr[0].graph['id'], edge, tuple(path))
				for edge_index in range(len(path)-1):
					SubtractBwResource(sn, (path[edge_index], path[edge_index+1]), vnr[0], edge)


def PathSplitting(sn, vnr_list, node_mapping_list, edge_mapping_list, request_queue):
	# Create the 'prob' object to contain the optimization problem data
	prob = pulp.LpProblem("Multi-commodity Flow", pulp.LpMinimize)
	# Build summation list for the objective function
	objFn = []

	# First create a total integer trailer flow variable, and tie it to the arc
	var = pulp.LpVariable("TrailerFlow(%s,%s)" % (str(i), str(j)), lowBound=0, cat=pulp.LpInteger)
	a_dict['dvTrailerFlow'] = var

	# The objective function is added to 'prob' first
	# lpSum takes a list of coefficients*LpVariables and makes a summation
	prob += pulp.lpSum(objFn), "Allocated BW"

	# Add the constraint for each commodity specific arc
	for vnr in vnr_list:
			prob += pulp.lpSum(objFn) <= vnr.edges[edge]['bw']
			prob += arcs[a]['dvFlows'][k] <= M * arcs[a]['dvIntree'][
				dest], " Consistency Arc (%s,%s) Commodity(%s,%s) " % (str(i), str(j), str(k_orig), str(k_dest))

	# Write out as a .LP file
	prob.writeLP("LinkSplitting.lp")

	# The problem is solved, in this case explicitly asking for Gurobi
	prob.solve(pulp.GUROBI())

	# The status of the solution is printed to the screen
	print("Status:", pulp.LpStatus[prob.status])


def Plotting(network):
	#pos = nx.spring_layout(network, scale=2)
	# Hard coded
	pos = { 'A': (10,20), 'B': (30, 30), 'C': (40,30), 'D': (30,20), 'E': (50,20), 'F': (20,10), 'G': (30,10), 'H': (40,10), 'I': (50,10)}
	nx.draw(network, pos)
	nx.draw_networkx_nodes(network, pos, nodelist=network.nodes(), node_color='b')
	nx.draw_networkx_edges(network, pos, nodelist=network.edges())
	network_node_labels = nx.get_node_attributes(network,"cpu")
	network_edge_labels = nx.get_edge_attributes(network,"bw")
	nx.draw_networkx_labels(network, pos, labels=network_node_labels)
	nx.draw_networkx_edge_labels(network, pos, with_labels=True, edge_labels=network_edge_labels)


# Substrate Network Input
asn = [70, 40, 60, 100, 80, 40, 60, 60, 60]
asl = 	[[0, 15, 0, 40, 0, 0, 0, 0, 0],
		 [15, 0, 15, 5, 0, 0, 0, 0, 0],
		 [0, 15, 0, 0, 15, 0, 0, 0, 0],
		 [40, 5, 0, 0, 40, 20, 10, 0, 0],
		 [0, 0, 15, 40, 0, 0, 0, 0, 10],
		 [0, 0, 0, 20, 0, 0, 0, 0, 0],
		 [0, 0, 0, 10, 0, 0, 0, 10, 0],
		 [0, 0, 0, 0, 0, 0, 10, 0, 10],
		 [0, 0, 0, 0, 10, 0, 0, 10, 0]]

# VNR 1 
cvn1 = [10, 10, 10]
cvl1 = 	[[0, 20, 20],
		 [20, 0, 0],
		 [20, 0, 0]]

# VNR 2
cvn2 = [5, 5]
cvl2 = 	[[0, 10],
		 [10, 0]]

# For lettering purposes
alphabet_dict = dict(zip(range(1,len(asl)+1), string.ascii_uppercase))

# Graph for Substrate Network
sn = nx.Graph()
GenerateNodes(sn, asn)
GenerateEdges(sn, asl)

# Graph for Input 1
vnr1 = nx.Graph(id=1, node_mapping_status=0, edge_mapping_status=0)
GenerateNodes(vnr1, cvn1)
GenerateEdges(vnr1, cvl1)

# Graph for Input 2
vnr2 = nx.Graph(id=2, node_mapping_status=0, edge_mapping_status=0)
GenerateNodes(vnr2, cvn2)
GenerateEdges(vnr2, cvl2)

plt.subplot(121)
Plotting(sn)

node_mapping_list = []
edge_mapping_list = []
request_queue = deque()

vnr_list = [vnr1, vnr2]
GetRevenue(vnr_list)

print("=== SN INFORMATION ===")
print("NODE DATA: ", sorted(sn.nodes.data()))
print("EDGE DATA: ", sorted(sn.edges.data()))
print("")

print("=== (BATCH) VNR INFORMATION ===")
for vnr in vnr_list:
	print("VNR ID# ", vnr[0].graph['id'])
	print("NODE DATA: ", sorted(vnr[0].nodes.data()))
	print("EDGE DATA: ", sorted(vnr[0].edges.data()))
	print("")

successful_node_mapping = GreedyNodeMapping(sn, vnr_list, node_mapping_list, request_queue)
GetRevenue(successful_node_mapping)

UnsplittableLinkMapping(sn, successful_node_mapping, node_mapping_list, edge_mapping_list, request_queue)

print("=== VNE RESULTS ===")
print("NODE MAPPING: ", node_mapping_list)
print("EDGE MAPPING: ", edge_mapping_list)
print("")

print("=== CURRENT SN RESOURCES ===")
print("NODE DATA: ", sorted(sn.nodes.data()))
print("EDGE DATA: ", sorted(sn.edges.data()))

plt.subplot(122)
Plotting(sn)

plt.show()