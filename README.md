# Versatile

## 2019 Changes in code to include content ID
### generate_with_contentid.py
Code for generating input files to algo

Generated files: 
+ substrate_network.txt
+ virtual_network_requests.txt

### substrate_network.txt
Input file including substrate network information with N nodes
+ Line 1 -> space-separated node ids
+ Line 2 -> space-separated cpu values 
+ Line 3 -> Empty line seperating information with content ids 
+ Next N (number of nodes) lines -> space-separated content id. 1 line per node 
+ Next Line -> Empty line seperating content ids with bandwith matrix
+ Next N (number of nodes) lines -> Matrix of bandwith values

### virtual_network_requests.txt
Input file which includes information of N virtual network requests

Format for each VNR
+ Line 1 -> VNR ID
+ Line 2 -> space-separated node ids
+ Line 3 -> space-separated cpu values
+ Line 4 -> space-separated delay values 
+ Line 5 -> space-separated maxhop values 
+ Line 6 -> space-separated cid values 
+ Next N (number of nodes) lines -> Matrix of bandwith values
